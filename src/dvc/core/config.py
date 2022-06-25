import enum
import re
import traceback

import psycopg2
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional, Union
import logging
from psycopg2._psycopg import connection
import os

from dvc.core.database import SupportedDatabaseFlavour, DBConnLike
from dvc.core.regex import get_matched_files_in_folder_by_regex
from dvc.core.exception import RequestedDatabaseFlavourNotSupportedException, InvalidDatabaseRevisionFilesException, \
    EnvironmentVariableNotSetException, Operation
from dvc.core.struct import DatabaseRevisionFile, DatabaseVersion


class ConfigDefault:
    # Default keys for Environment variable
    KEY__DATABASE_REVISION_SQL_FILES_FOLDER = "DVC__DATABASE_REVISION_SQL_FILES_FOLDER"
    KEY__USER = "DVC__USER"
    KEY__PASSWORD = "DVC__PASSWORD"
    KEY__HOST = "DVC__HOST"
    KEY__PORT = "DVC__PORT"
    KEY__DBNAME = "DVC__DBNAME"
    KEY__DBFLAVOUR = "DVC__DBFLAVOUR"
    KEY__LOGGING_LEVEL = "DVC__LOGGING_LEVEL"

    # Default values for environment variables
    VAL__DATABASE_REVISION_SQL_FILES_FOLDER = "sample_revision_sql_files"
    VAL__USER = ""
    VAL__PASSWORD = ""
    VAL__HOST = ""
    VAL__PORT = 5432
    VAL__DBNAME = ""
    VAL__DBFLAVOUR = "postgres"
    VAL__LOGGING_LEVEL: str = logging._levelToName[logging.INFO]

    # Default values for config file
    VAL__FilE_NAME: str = "config.yaml"
    VAL__FILE_PATH: Path = Path(VAL__FilE_NAME)

    @classmethod
    def get_config_dict(
            cls,
            database_revision_sql_files_folder: str,
            user: str,
            password: str,
            host: str,
            port: int,
            dbname: str,
            dbflavour: str,
            logging_level: int,
            as_file=False
    ):
        """

        :param database_revision_sql_files_folder:
        :param user:
        :param password:
        :param host:
        :param port:
        :param dbname:
        :param dbflavour:
        :param logging_level: Assumed to be integer value
        :param as_file: whether to dump the dict as file.
        :return:
        """
        CONFIG_DICT: Dict = {
            "logging_level": logging_level if not as_file else logging._levelToName[logging_level],
            "database_revision_sql_files_folder": database_revision_sql_files_folder,
            "credentials": {
                "user": user,
                "password": password,
                "host": host,
                "port": port,
                "dbname": dbname,
                "dbflavour": dbflavour,
            }
        }
        return CONFIG_DICT


class ConfigFileWriter:
    """
    Read Config Files (in different formats) to Python Dictionary
    """

    def __init__(self,
                 config_file_path: Union[Path, str] = ConfigDefault.VAL__FILE_PATH,
                 ):
        if type(config_file_path) == str:
            self.config_file_path = Path(config_file_path)
        elif isinstance(config_file_path, Path):
            self.config_file_path = config_file_path
        else:
            raise TypeError(
                f"config file path must be of either type str or is instance of Path. Yours is {type(config_file_path)}")

    def write_to_yaml(self) -> None:
        default_config_dict: Dict = ConfigDefault.get_config_dict(
            database_revision_sql_files_folder=ConfigDefault.VAL__DATABASE_REVISION_SQL_FILES_FOLDER,
            user=ConfigDefault.VAL__USER,
            password=ConfigDefault.VAL__PASSWORD,
            host=ConfigDefault.VAL__HOST,
            port=ConfigDefault.VAL__PORT,
            dbname=ConfigDefault.VAL__DBNAME,
            dbflavour=ConfigDefault.VAL__DBFLAVOUR,
            logging_level=logging._nameToLevel[ConfigDefault.VAL__LOGGING_LEVEL],
            as_file=True
        )

        if not self.config_file_path.exists():
            logging.info(f"Now generating default config file {self.config_file_path}")
            with open(self.config_file_path, 'w') as default_config_file:
                yaml.dump(default_config_dict, default_config_file, default_flow_style=False)
        else:
            logging.info(f"{self.config_file_path} already exists! Do nothing.")


class ConfigReader:
    """
    Read Config (in different formats) to Python Dictionary

    Precedence in descending order
    1. Config File
    2. Environment Variable
    """

    def __init__(self,
                 config_file_path: Union[Path, str] = ConfigDefault.VAL__FILE_PATH,
                 ):
        if type(config_file_path) == str:
            self.config_file_path = Path(config_file_path)
        elif isinstance(config_file_path, Path):
            self.config_file_path = config_file_path
        else:
            raise TypeError(f"config file path must be of either type str or Path. Yours is {type(config_file_path)}")

        # read user config
        self.user_config = self._read_user_config()
        self.requested_db_flavour = self._read_requested_db_flavour()
        self.logging_level = self._read_logging_level()

    def _read_logging_level(self) -> int:
        user_config = self.user_config
        logging_level: int = user_config['logging_level']
        return logging_level

    def _read_requested_db_flavour(self) -> str:
        user_config = self.user_config
        requested_db_flavour: str = user_config['credentials']['dbflavour']
        return requested_db_flavour

    def _read_user_config(self) -> Dict:
        """
        Check if config_file_path points to an existing file.
        If yes, read config from the file.
        If not, read config from env var.

        :return:
        """
        if self.config_file_path.is_file() and self.config_file_path.exists():
            user_config = self._read_from_yaml()
        else:
            user_config = self._read_from_environment()
        return user_config

    def _read_from_yaml(self) -> Dict:
        """
        Read User Config from Yaml File
        """
        logging.info(f"Reading config from file...")
        with open(self.config_file_path, 'r', encoding='utf-8') as config_file:
            user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)

        try:
            # Assume is value
            user_config['logging_level'] = int(user_config['logging_level'])
        except ValueError as e:
            try:
                # Assume is string
                user_config['logging_level'] = logging._nameToLevel[user_config['logging_level']]
            except KeyError as e:
                logging.error("logging_level must be one of the below:")
                logging.error(logging._nameToLevel)
                raise

        return user_config

    def _read_from_environment(self) -> Dict:
        """
        Read User Config from environment variables
        """
        logging.info(f"Reading config from environment...")

        # Raise Key error if the environment variable is not set
        try:
            database_revision_sql_files_folder = os.environ[ConfigDefault.KEY__DATABASE_REVISION_SQL_FILES_FOLDER]
            host = os.environ[ConfigDefault.KEY__HOST]
            port = int(os.environ[ConfigDefault.KEY__PORT])
            user = os.environ[ConfigDefault.KEY__USER]
            password = os.environ[ConfigDefault.KEY__PASSWORD]
            dbname = os.environ[ConfigDefault.KEY__DBNAME]
            dbflavour = os.environ[ConfigDefault.KEY__DBFLAVOUR]
            logging_level = os.environ[ConfigDefault.KEY__LOGGING_LEVEL]
        except KeyError as err:
            missing_env_var = err.args[0]
            raise EnvironmentVariableNotSetException(missing_env_var)

        # Convert logging_level
        try:
            # Assume is value
            logging_level = int(logging_level)
        except ValueError as e:
            try:
                # Assume is string
                logging_level = logging._nameToLevel[logging_level]
            except KeyError as e:
                logging.error("logging_level must be one of the below:")
                logging.error(logging._nameToLevel)
                raise

        user_config = ConfigDefault.get_config_dict(
            database_revision_sql_files_folder=database_revision_sql_files_folder,
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            dbflavour=dbflavour,
            port=port,
            logging_level=logging_level
        )
        return user_config


class DatabaseRevisionFilesManager:
    """
    Manager all Database Revision Files
    """

    class Pointer:
        """
        Head: ALl the way to the latest
        """
        HEAD = 'head'
        BASE = 'base'

    def __init__(self,
                 config_file_reader: ConfigReader,
                 ):
        self.config_file_reader = config_file_reader
        self.database_revision_files_folder = self._get_database_revision_files_folder()
        self.all_database_revision_files = self._scan_database_revision_files()

    def _scan_database_revision_files(self) -> List[DatabaseRevisionFile]:
        """
        Return all the available database revision files
        :return:
        """
        candidate_database_revision_files: List[DatabaseRevisionFile] = []
        database_revision_files_folder = self.database_revision_files_folder

        logging.debug("---Scanning database revision files----")
        for file_or_dir in database_revision_files_folder.glob('**/*'):
            file_or_dir: Path = file_or_dir
            logging.debug(file_or_dir)
            if file_or_dir.is_file():
                candidate_database_revision_file = DatabaseRevisionFile(file_or_dir)
                candidate_database_revision_files.append(candidate_database_revision_file)
        logging.debug("---/Scanning database revision files----")

        return candidate_database_revision_files

    def _get_database_revision_files_folder(self) -> Path:
        """
        Get database revision files folder
        :return:
        """
        return Path(self.config_file_reader.user_config['database_revision_sql_files_folder'])

    def create_database_revision_files_folder(self) -> None:
        """
        Safely create the database revision files folder.
        """
        database_revision_sql_folder = self.database_revision_files_folder
        database_revision_sql_folder_path = Path(database_revision_sql_folder)

        if database_revision_sql_folder_path.exists():
            logging.info(f"{database_revision_sql_folder_path} already exists. Do nothing")
        else:
            logging.info("Generating database revision folder")
            database_revision_sql_folder_path.mkdir(parents=True)

    def _raise_for_status(self,
                          database_revision_files: List[DatabaseRevisionFile],
                          steps: int,
                          ) -> None:
        """
        Raise Exception when number of database revision files are not the same as number of steps
        :param database_revision_files:
        :param steps:
        :return:
        """
        # Step 3: Raise Error if number of returned revision files are different from the number of steps specified
        logging.debug(f"database revision files: {database_revision_files}")
        logging.debug(f"steps: {steps}")

        if len(database_revision_files) > abs(steps):
            raise InvalidDatabaseRevisionFilesException(
                config_file_path=self.database_revision_files_folder,
                status=InvalidDatabaseRevisionFilesException.Status.MORE_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED,
                database_revision_file_paths=[actual_revision_file.file_path for actual_revision_file in
                                              database_revision_files],
            )
        elif len(database_revision_files) < abs(steps):
            raise InvalidDatabaseRevisionFilesException(
                config_file_path=self.database_revision_files_folder,
                status=InvalidDatabaseRevisionFilesException.Status.FEWER_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED,
                database_revision_file_paths=[actual_revision_file.file_path for actual_revision_file in
                                              database_revision_files],
            )
        else:
            # All good
            pass

    def get_target_database_revision_files_by_pointer(
            self,
            current_database_version: DatabaseVersion,
            candidate_database_revision_files: List[DatabaseRevisionFile],
            pointer: Pointer,
    ) -> List[DatabaseRevisionFile]:
        """
        Given current database version and pointer, filter for target database revision files in the folder

        :param current_database_version:
        :param candidate_database_revision_files:
        :return:
        """
        # Step 1: Deduce the number of steps
        current_database_version_number = current_database_version.version_number

        # create a reference database revision file
        if pointer == self.Pointer.HEAD:
            reference_database_revision_file = DatabaseRevisionFile.get_dummy_revision_file(
                revision=f'RV{current_database_version_number + 1}',
                operation_type=Operation.Upgrade, )
            target_database_revision_files = [file for file in candidate_database_revision_files if
                                              file >= reference_database_revision_file]

            # Closest to current db version. Ascending order
            target_database_revision_files.sort(reverse=False)

            if len(target_database_revision_files) == 0:
                deduced_steps = 0
            else:
                deduced_steps = target_database_revision_files[-1].revision_number - current_database_version_number

        elif pointer == self.Pointer.BASE:
            reference_database_revision_file = DatabaseRevisionFile.get_dummy_revision_file(
                revision=f'RV{current_database_version_number}',
                operation_type=Operation.Downgrade, )

            # Closest to current db version. Descending order
            target_database_revision_files = [file for file in candidate_database_revision_files if
                                              file <= reference_database_revision_file]

            target_database_revision_files.sort(reverse=True)

            if len(target_database_revision_files) == 0:
                deduced_steps = 0
            else:
                deduced_steps = current_database_version_number - target_database_revision_files[-1].revision_number + 1

        else:
            raise ValueError(f"Unhandled Pointer {pointer}!")

        self._raise_for_status(database_revision_files=target_database_revision_files,
                               steps=deduced_steps,
                               )

        return target_database_revision_files


    def get_target_database_revision_files_by_steps(
            self,
            current_database_version: DatabaseVersion,
            steps: int,
            candidate_database_revision_files: List[DatabaseRevisionFile],
    ) -> List[DatabaseRevisionFile]:
        """
        Given current database version and number of steps, filter for target database revision files in the folder.

        :return:
        """

        # Step 1: Get a list of dummy database revision files
        current_database_version_number = current_database_version.version_number
        target_database_version = DatabaseVersion(version=f"V{current_database_version_number + steps}")

        dummy_revision_files: List[DatabaseRevisionFile] = target_database_version - current_database_version
        actual_revision_files: List[DatabaseRevisionFile] = []

        # Step 2: Loop folder for actual files
        for dummy_revision_file in dummy_revision_files:
            logging.debug(f"Looking for Revision File with revision number {dummy_revision_file.revision_number}.....")
            for candidate_database_revision_file in candidate_database_revision_files:
                if dummy_revision_file == candidate_database_revision_file:
                    actual_revision_files.append(candidate_database_revision_file)

        self._raise_for_status(database_revision_files=actual_revision_files,
                               steps=steps,
                               )
        return actual_revision_files


class DatabaseConnectionFactory:
    """
    Return connections for various databases
    """
    MAPPING = {
        SupportedDatabaseFlavour.Postgres: 'self.pgconn'
    }

    def __init__(self,
                 config_reader: ConfigReader,
                 ):
        """

        :param config_reader: Config Reader
        """
        self.config_reader = config_reader

    def validate_requested_database_flavour(
            self) -> SupportedDatabaseFlavour:
        """
        Validate if requested database flavour is supported

        :return:
        """
        try:
            supported_user_db_flavour = SupportedDatabaseFlavour(self.config_reader.requested_db_flavour)
        except ValueError as e:
            logging.error(traceback.format_exc())
            raise RequestedDatabaseFlavourNotSupportedException(
                requested_database_flavour=self.config_reader.requested_db_flavour)
        return supported_user_db_flavour

    @property
    def conn(self) -> DBConnLike:
        """
        Return the expected connection object for different database flavours
        :return:
        """
        supported_db_flavour = self.validate_requested_database_flavour()
        # Map Supported database flavours to different connections
        return eval(self.__class__.MAPPING[supported_db_flavour])

    @property
    def pgconn(self) -> connection:
        """
        Return Postgres Database Connection

        :return:
        """
        dbname = self.config_reader.user_config['credentials']['dbname']
        user = self.config_reader.user_config['credentials']['user']
        password = self.config_reader.user_config['credentials']['password']
        port = self.config_reader.user_config['credentials']['port']
        host = self.config_reader.user_config['credentials']['host']

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
        return conn
