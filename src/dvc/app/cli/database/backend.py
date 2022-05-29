from typing import Optional, List
from pathlib import Path
import re
import logging
from psycopg2._psycopg import connection

from dvc.core.database import SupportedDatabaseFlavour

from dvc.core.database.postgres import PostgresSQLFileExecutor
from dvc.core.database.mysql import MySQLSQLFileExecutor
from dvc.core.database.bigquery import BigQuerySQLFileExecutor

from dvc.core.struct import Operation
from dvc.core.config import Default, DatabaseRevisionFilesManager, ConfigFileReader, DatabaseConnectionFactory
from dvc.core.file import validate_file_exist


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


class DatabaseInteractor:
    """
    Exposes API to interact with Various Database flavours
    """
    MAPPING = {
        SupportedDatabaseFlavour.Postgres: lambda conn: PostgresSQLFileExecutor(conn)
    }

    def __init__(self,
                 config_file_path_str: Optional[str],
                 ):
        self.config_file_path: Optional[Path] = None if config_file_path_str is None else Path(config_file_path_str)

    @property
    def config_file_reader(self):
        if self.config_file_path is None:
            config_file_reader = ConfigFileReader(Default.CONFIG_FILE_PATH)
        else:
            validate_file_exist(self.config_file_path)
            config_file_reader = ConfigFileReader(self.config_file_path)
        return config_file_reader

    @property
    def conn(self):
        config_file_reader = self.config_file_reader
        conn = DatabaseConnectionFactory(config_file_reader=config_file_reader).conn
        return conn

    @property
    def sql_file_executor(self):
        config_file_reader = self.config_file_reader
        conn = self.conn
        supported_db_flavour = DatabaseConnectionFactory(config_file_reader=config_file_reader).validate_requested_database_flavour()
        sql_file_executor = self.__class__.MAPPING[supported_db_flavour](conn)
        return sql_file_executor
