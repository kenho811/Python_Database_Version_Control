import psycopg2
import yaml
from pathlib import Path
from typing import Dict, List
import logging
from psycopg2._psycopg import connection


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


def read_config_file(config_file_path: Path = Default.CONFIG_FILE_PATH, ) -> Dict:
    with open(config_file_path, 'r') as config_file:
        user_config: Dict = yaml.load(config_file, Loader=yaml.FullLoader)
    return user_config


def get_postgres_connection(config_file_path: Path = Default.CONFIG_FILE_PATH,) -> connection:
    user_config = read_config_file(config_file_path)
    dbname = user_config['credentials']['dbname']
    user = user_config['credentials']['user']
    password = user_config['credentials']['password']
    port = user_config['credentials']['port']
    host = user_config['credentials']['host']

    conn = psycopg2.connect(dbname=dbname, user=user, password=password, port=port, host=host)
    return conn


def get_database_revision_sql_files(config_file_path: Path = Default.CONFIG_FILE_PATH) -> List[Path]:
    """
    Loop recursively for all files in folder
    :return:
    """
    sql_files: List[Path] = []

    user_config = read_config_file(config_file_path)

    database_revision_sql_files_folder = user_config['database_revision_sql_files_folder']
    for file_or_dir in Path(database_revision_sql_files_folder).glob('**/*'):
        if file_or_dir.is_file() and file_or_dir.suffix == '.sql':
            sql_files.append(file_or_dir)

    return sql_files
