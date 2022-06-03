import re
import traceback

import psycopg2
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from psycopg2._psycopg import connection
import os

from dvc.core.database import SupportedDatabaseFlavour
from dvc.core.regex import get_matched_files_in_folder_by_regex
from dvc.core.exception import RequestedDatabaseFlavourNotSupportedException, InvalidDatabaseRevisionFilesException, \
    EnvironmentVariableNotSetException


class ConfigDefault:
    # Default keys for Environment variable
    KEY__DATABASE_REVISION_SQL_FILES_FOLDER = "DVC__DATABASE_REVISION_SQL_FILES_FOLDER"
    KEY__USER = "DVC__USER"
    KEY__PASSWORD = "DVC__PASSWORD"
    KEY__HOST = "DVC__HOST"
    KEY__PORT = "DVC__PORT"
    KEY__DBNAME = "DVC__DBNAME"
    KEY__DBFLAVOUR = "DVC__DBFLAVOUR"

    # Default values for environment variables
    VAL__DATABASE_REVISION_SQL_FILES_FOLDER = "sample_revision_sql_files"
    VAL__USER = ""
    VAL__PASSWORD = ""
    VAL__HOST = ""
    VAL__PORT = 5432
    VAL__DBNAME = ""
    VAL__DBFLAVOUR = "postgres"

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
            dbflavour: str

    ):
        CONFIG_DICT: Dict = {
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
                 config_file_path: Path = ConfigDefault.VAL__FILE_PATH,
                 ):
        self.config_file_path = config_file_path

    def write_to_yaml(self) -> None:
        default_config_dict: Dict = ConfigDefault.get_config_dict(
            database_revision_sql_files_folder=ConfigDefault.VAL__DATABASE_REVISION_SQL_FILES_FOLDER,
            user=ConfigDefault.VAL__USER,
            password=ConfigDefault.VAL__PASSWORD,
            host=ConfigDefault.VAL__HOST,
            port=ConfigDefault.VAL__PORT,
            dbname=ConfigDefault.VAL__DBNAME,
            dbflavour=ConfigDefault.VAL__DBFLAVOUR,
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
                 config_file_path: Path = ConfigDefault.VAL__FILE_PATH,
                 ):
        self.config_file_path = config_file_path

    @property
    def user_config(self) -> Dict:
        """
        Initialise user config

        Precedence in descending order
        1. Config File
        2. Environment Variable
        """
        if self.config_file_path.is_file():
            user_config = self._read_from_yaml()
        else:
            user_config = self._read_from_environment()
        return user_config

    @property
    def requested_db_flavour(self) -> str:
        """
        Read requested_db_flavour from user_config
        """
        user_config = self.user_config
        requested_db_flavour: str = user_config['credentials']['dbflavour']
        return requested_db_flavour

    def _read_from_yaml(self) -> Dict:
        """
        Read User Config from Yaml File
        """
        logging.info(f"Reading config from file...")
        with open(self.config_file_path, 'r', encoding='utf-8') as config_file:
            user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)
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
        except KeyError as err:
            missing_env_var = err.args[0]
            raise EnvironmentVariableNotSetException(missing_env_var)

        user_config = ConfigDefault.get_config_dict(
            database_revision_sql_files_folder=database_revision_sql_files_folder,
            host=host,
            user=user,
            password=password,
            dbname=dbname,
            dbflavour=dbflavour,
            port=port,
        )
        return user_config


class DatabaseRevisionFilesManager:
    """
    Manager all Database Revision Files
    """
    STANDARD_RV_FILE_FORMAT = r'RV[0-9]*__.*\.(upgrade|downgrade)\.sql'

    def __init__(self,
                 config_file_reader: ConfigReader,
                 ):
        self.config_file_reader = config_file_reader

    @property
    def database_revision_files_folder(self) -> Path:
        return Path(self.config_file_reader.user_config['database_revision_sql_files_folder'])

    def validate_database_revision_sql_files(self):
        # Step 1: Check revision file name
        prog = re.compile(self.__class__.STANDARD_RV_FILE_FORMAT)

        for file in self.database_revision_files_folder.glob('**/*'):
            if file.is_file():
                match = prog.match(file.name)
                if not match:
                    raise InvalidDatabaseRevisionFilesException(
                        file_path=file,
                        status=InvalidDatabaseRevisionFilesException.Status.NON_CONFORMANT_REVISION_FILE_NAME_EXISTS)

        # Step 2: Check no duplicates

    def create_database_revision_files_folder(self):
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

    def get_database_revision_files_by_regex(self,
                                             file_name_regex: str,
                                             ) -> List[Path]:
        """
        Loop recursively for all files in a given folder.
        Return those files whose name satisfy the regex.
        :return:
        """
        database_revision_files_folder = self.database_revision_files_folder
        files: List[Path] = get_matched_files_in_folder_by_regex(
            folder_path=database_revision_files_folder,
            file_name_regex=file_name_regex
        )
        return files


class DatabaseConnectionFactory:
    """
    Return connections for various databases
    """
    MAPPING = {
        SupportedDatabaseFlavour.Postgres: 'self.pgconn'
    }

    def __init__(self,
                 config_file_reader: ConfigReader,
                 ):
        self.config_file_reader = config_file_reader

    def validate_requested_database_flavour(
            self) -> SupportedDatabaseFlavour:
        """
        Validate if requested database flavour is supported
        """
        try:
            supported_user_db_flavour = SupportedDatabaseFlavour(self.config_file_reader.requested_db_flavour)
        except ValueError as e:
            logging.error(traceback.format_exc())
            raise RequestedDatabaseFlavourNotSupportedException(
                requested_database_flavour=self.config_file_reader.requested_db_flavour)
        return supported_user_db_flavour

    @property
    def conn(self) -> Any:
        """
        Return the expected connection
        """
        supported_db_flavour = self.validate_requested_database_flavour()
        # Map Supported database flavours to different connections
        return eval(self.__class__.MAPPING[supported_db_flavour])

    @property
    def pgconn(self) -> connection:
        """
        Return Postgres Database Connection
        """
        dbname = self.config_file_reader.user_config['credentials']['dbname']
        user = self.config_file_reader.user_config['credentials']['user']
        password = self.config_file_reader.user_config['credentials']['password']
        port = self.config_file_reader.user_config['credentials']['port']
        host = self.config_file_reader.user_config['credentials']['host']

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
        return conn


def get_revision_number_from_database_revision_file(database_revision_file_path: Path) -> int:
    """
    """
    revision_number = int(database_revision_file_path.name.split('__')[0][2:])
    return revision_number
