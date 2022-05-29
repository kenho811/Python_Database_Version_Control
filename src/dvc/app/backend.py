from typing import Optional, List
from pathlib import Path
import re
import logging
from psycopg2._psycopg import connection

from dvc.core.struct import Operation
from dvc.core.config import Default, DatabaseRevisionFilesManager, ConfigFileReader, DatabaseConnectionFactory


def get_target_database_revision_sql_files(
        config_file_reader: ConfigFileReader,
        operation_type: Operation,
        target_revision_version: str,
) -> List[Path]:
    file_name_regex = f"{target_revision_version}__.*\.{operation_type.value}\.sql"

    # Get path of Database Revision SQL files
    db_rv_files_man = DatabaseRevisionFilesManager(config_file_reader)
    matched_paths = db_rv_files_man.get_database_revision_files_by_regex(file_name_regex=file_name_regex)
    return matched_paths


def validate_file_exist(file_path: Path) -> None:
    if not file_path.is_file():
        err_msg = f"File Path {file_path} does not exist!"
        logging.error(err_msg)
        raise FileNotFoundError(err_msg)


def get_database_connection(config_file_path_str: str) -> connection:
    """
    Given config file path, give the database connection
    """
    if config_file_path_str is None:
        config_file_reader = ConfigFileReader(Default.CONFIG_FILE_PATH)
    else:
        config_file_path_str = Path(config_file_path_str)
        validate_file_exist(config_file_path_str)
        config_file_reader = ConfigFileReader(config_file_path_str)

    return DatabaseConnectionFactory(config_file_reader=config_file_reader).conn
