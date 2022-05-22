import psycopg2
import yaml
from pathlib import Path
from typing import Dict, List, Any, Optional
import logging
from psycopg2._psycopg import connection

from dvc.core.database import SupportedDatabaseFlavour
from dvc.core.regex import get_matched_files_in_folder_by_regex


class Default:
    CONFIG_FilE_NAME: str = "config.yaml"
    CONFIG_FILE_PATH: Path = Path(CONFIG_FilE_NAME)


class ConfigFileWriter:
    """
    Read Config Files (in different formats) to Python Dictionary
    """
    CONFIG_FILE_TEMPLATE: Dict = {
        "database_revision_sql_files_folder": "sample_revision_sql_files",
        "credentials": {
            "user": "",
            "password": "",
            "host": "",
            "port": 5432,
            "dbname": "",
            "dbflavour": "postgres"

        }
    }

    def __init__(self,
                 config_file_path: Path = Default.CONFIG_FILE_PATH,
                 ):
        self.config_file_path = config_file_path

    def write_to_yaml(self) -> None:
        if not self.config_file_path.exists():
            logging.info(f"Now generating default config file {self.config_file_path}")
            with open(self.config_file_path, 'w') as default_config_file:
                yaml.dump(self.__class__.CONFIG_FILE_TEMPLATE, default_config_file, default_flow_style=False)
        else:
            logging.info(f"{self.config_file_path} already exists! Do nothing.")


class ConfigFileReader:
    """
    Read Config Files (in different formats) to Python Dictionary
    """

    def __init__(self,
                 config_file_path: Path = Default.CONFIG_FILE_PATH,
                 ):
        self.config_file_path = config_file_path

    @property
    def user_config(self) -> Dict:
        return self.read_from_yaml()

    def read_from_yaml(self) -> Dict:
        with open(self.config_file_path, 'r', encoding='utf-8') as config_file:
            user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)
        return user_config


class DatabaseRevisionFilesManager:
    """
    Manager all Database Revision Files
    """

    def __init__(self,
                 config_file_reader: ConfigFileReader,
                 ):
        self.config_file_reader = config_file_reader

    @property
    def database_revision_files_folder(self) -> Path:
        return Path(self.config_file_reader.user_config['database_revision_sql_files_folder'])

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
    def __init__(self,
                 config_file_reader: ConfigFileReader,
                 ):
        self.config_file_reader = config_file_reader

    @property
    def supported_user_database_flavour(self) -> SupportedDatabaseFlavour:
        user_db_flavour: str = self.config_file_reader.user_config['credentials']['dbflavour']
        try:
            supported_user_db_flavour = SupportedDatabaseFlavour(user_db_flavour)
        except Exception as e:
            logging.error(f"Supported Database Flavours are :")
            logging.error([e.name for e in SupportedDatabaseFlavour])
            raise

        return supported_user_db_flavour

    @property
    def conn(self) -> Any:
        """
        Generic getter for any database connection
        """
        supported_user_database_flavour = self.supported_user_database_flavour
        if supported_user_database_flavour == SupportedDatabaseFlavour.Postgres:
            return self.pgconn
        else:
            raise ValueError(f"Not supported database flavour {supported_user_database_flavour}")

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
