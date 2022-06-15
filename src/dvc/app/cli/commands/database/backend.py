import traceback
from typing import Optional, List
from pathlib import Path
import re
import logging
from psycopg2._psycopg import connection

from dvc.core.database import SupportedDatabaseFlavour

from dvc.core.database.postgres import PostgresSQLFileExecutor
from dvc.core.database.mysql import MySQLSQLFileExecutor
from dvc.core.database.bigquery import BigQuerySQLFileExecutor

from dvc.core.struct import Operation, DatabaseVersion, DatabaseRevision
from dvc.core.config import ConfigDefault, DatabaseRevisionFilesManager, ConfigReader, DatabaseConnectionFactory
from dvc.core.file import validate_file_exist
from dvc.core.exception import InvalidDatabaseRevisionFilesException, DatabaseConnectionFailureException, OperationNotAccountedForException


def get_target_database_revision_sql_files(
        config_file_reader: ConfigReader,
        operation_type: Operation,
        target_revision_version: str,
) -> List[Path]:
    file_name_regex = rf"{target_revision_version}__.*\.{operation_type.value}\.sql"

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

    def ping(self):
        try:
            conn = self.conn
        except Exception as e:
            logging.error(traceback.format_exc())
            raise DatabaseConnectionFailureException
        else:
            logging.info("Database connection looks good!")

    def get_latest_database_version(self) -> DatabaseVersion:
        latest_database_version: DatabaseVersion = self.sql_file_executor.get_latest_database_version()
        return latest_database_version

    def execute_sql_files(self,
                          operation_type: Operation,
                          sql_files_paths: List[Path],
                          mark_only: bool = False,
                          ) -> None:

        sql_file_path = sql_files_paths[0]

        if mark_only:
            logging.info(f"Now only marking {sql_file_path} to metadata table")
            database_revision = DatabaseRevision(
                executed_sql_file_path_applied=sql_file_path,
                operation=operation_type
            )
            self.sql_file_executor._write_database_revision_metadata(database_revision=database_revision)
        else:
            logging.info(f"Now applying {sql_file_path} and marking to metadata table")
            database_revision = DatabaseRevision(
                executed_sql_file_path_applied=sql_file_path,
                operation=operation_type
            )
            self.sql_file_executor.execute_database_revision(database_revision=database_revision)

    def get_target_revision_sql_files(self,
                                      operation_type: Operation,
                                      steps: int = 1
                                      ) -> List[Path]:
        """
        Helper to get target revision sql files

        :param operation_type: Specify the operation type
        :param steps: Specify how many steps ahead/ backwards.
        :return:
        """
        # Step 1: Get target revision files
        if operation_type == Operation.Upgrade:
            target_revision_version = self.get_latest_database_version().next_upgrade_revision_version
        elif operation_type == Operation.Downgrade:
            target_revision_version = self.get_latest_database_version().next_downgrade_revision_version
        else:
            raise OperationNotAccountedForException(operation_type=operation_type)

        # Step 2: Get target revision files
        if steps == 1:
            target_revision_files: List[Path] = get_target_database_revision_sql_files(
                config_file_reader=self.config_file_reader,
                operation_type=operation_type,
                target_revision_version=target_revision_version,
            )
        else:
            raise NotImplementedError("Steps other than 1 not implemented!")

        # Step 3: Raise Error if number of returned revision files are different from the number of steps specified
        if len(target_revision_files) > steps:
            raise InvalidDatabaseRevisionFilesException(
                file_path=self.config_file_path,
                status=InvalidDatabaseRevisionFilesException.Status.MORE_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED
            )
        elif len(target_revision_files) < steps:
            raise InvalidDatabaseRevisionFilesException(
                file_path=self.config_file_path,
                status=InvalidDatabaseRevisionFilesException.Status.FEWER_REVISION_SQL_FILES_FOUND_THAN_REQUIRED_STEPS_SPECIFIED
            )

        return target_revision_files

    @property
    def config_file_reader(self):
        if self.config_file_path is None:
            config_file_reader = ConfigReader(ConfigDefault.VAL__FILE_PATH)
        else:
            validate_file_exist(self.config_file_path)
            config_file_reader = ConfigReader(self.config_file_path)
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
        supported_db_flavour = DatabaseConnectionFactory(
            config_file_reader=config_file_reader).validate_requested_database_flavour()
        sql_file_executor = self.__class__.MAPPING[supported_db_flavour](conn)
        return sql_file_executor
