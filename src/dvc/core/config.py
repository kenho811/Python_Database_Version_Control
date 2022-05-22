import psycopg2
import yaml
from pathlib import Path
from typing import Dict, List
import logging
from psycopg2._psycopg import connection
import re

from dvc.core.regex import get_matched_files_in_folder_by_regex


class Default:
    CONFIG_FilE_NAME = "config.yaml"
    CONFIG_FILE_PATH = Path(CONFIG_FilE_NAME)


CONFIG_FILE_TEMPLATE: Dict = {
    "database_revision_sql_files_folder": "sample_revision_sql_files",
    "credentials": {
        "user": "",
        "password": "",
        "host": "",
        "port": 5432,
        "dbname": "",
    }
}


def write_default_config_file():
    if not Default.CONFIG_FILE_PATH.exists():
        logging.info(f"Now generating default config file {Default.CONFIG_FILE_PATH}")
        with open(Default.CONFIG_FILE_PATH, 'w') as default_config_file:
            yaml.dump(CONFIG_FILE_TEMPLATE, default_config_file, default_flow_style=False)
    else:
        logging.info(f"{Default.CONFIG_FILE_PATH} already exists! Do nothing.")


def generate_database_revision_sql_folder(config_file_path: Path) -> None:
    config: Dict = read_config_file(config_file_path)
    database_revision_sql_folder = config['database_revision_sql_files_folder']
    database_revision_sql_folder_path = Path(database_revision_sql_folder)

    if database_revision_sql_folder_path.exists():
        logging.info(f"{database_revision_sql_folder_path} already exists. Do nothing")
    else:
        logging.info("Generating database revision folder")
        database_revision_sql_folder_path.mkdir(parents=True)


class ConfigFileReader:
    """
    Read Config Files (in different formats) to Python Dictionary
    """

    def __init__(self,
                 config_file_path: Path = Default.CONFIG_FILE_PATH,
                 ):
        self.config_file_path = config_file_path
        self.user_config: Dict = self._read_from_yaml()

    def _read_from_yaml(self) -> Dict:
        with open(self.config_file_path, 'r', encoding='utf-8') as config_file:
            user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)
        return user_config


class DatabaseRevisionFilesManager(ConfigFileReader):
    """
    Manager all Database Revision Files
    """

    def __init__(self,
                 config_file_path: Path = Default.CONFIG_FILE_PATH,
                 ):
        super(DatabaseRevisionFilesManager, self).__init__(config_file_path)

    @property
    def database_revision_files_folder(self) -> Path:
        return Path(self.user_config['database_revision_sql_files_folder'])

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


class DatabaseConnectionFactory(ConfigFileReader):
    """
    Return connections for various databases
    """

    def __init__(self,
                 config_file_path: Path = Default.CONFIG_FILE_PATH,
                 ):
        super(DatabaseConnectionFactory, self).__init__(config_file_path)

    @property
    def pgconn(self) -> connection:
        """
        Return Postgres Database Connection
        """
        dbname = self.user_config['credentials']['dbname']
        user = self.user_config['credentials']['user']
        password = self.user_config['credentials']['password']
        port = self.user_config['credentials']['port']
        host = self.user_config['credentials']['host']

        conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
        return conn


def read_config_file(config_file_path: Path = Default.CONFIG_FILE_PATH, ) -> Dict:
    with open(config_file_path, 'r', encoding='utf-8') as config_file:
        user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)
    return user_config


def get_revision_number_from_database_revision_file(database_revision_file_path: Path) -> int:
    """
    """
    revision_number = int(database_revision_file_path.name.split('__')[0][2:])
    return revision_number
