import psycopg2
import yaml
from pathlib import Path
from typing import Dict, List
import logging
from psycopg2._psycopg import connection
import re


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


def read_config_file(config_file_path: Path = Default.CONFIG_FILE_PATH, ) -> Dict:
    with open(config_file_path, 'r') as config_file:
        user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)
    return user_config




def get_postgres_connection(config_file_path: Path = Default.CONFIG_FILE_PATH, ) -> connection:
    user_config = read_config_file(config_file_path)
    dbname = user_config['credentials']['dbname']
    user = user_config['credentials']['user']
    password = user_config['credentials']['password']
    port = user_config['credentials']['port']
    host = user_config['credentials']['host']

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
    return conn


def get_matched_files_in_folder_by_regex(folder_path: Path,
                                         file_name_regex: str,
                                         ) -> List[Path]:
    """
    Loop recursively for all files in a given folder.
    Return those files whose name satisfy the regex.
    :return:
    """
    matched_files_paths: List[Path] = []
    logging.info(f"Looking for the files with regex: {file_name_regex} in folder {folder_path}")
    prog = re.compile(file_name_regex)

    for file_or_dir in folder_path.glob('**/*'):
        file_or_dir: Path = file_or_dir
        if file_or_dir.is_file() and prog.match(file_or_dir.name):
            matched_files_paths.append(file_or_dir)

    return matched_files_paths


def get_revision_number_from_database_revision_file(database_revision_file_path: Path) -> int:
    """
    """
    revision_number = int(database_revision_file_path.name.split('__')[0][2:])
    return revision_number
