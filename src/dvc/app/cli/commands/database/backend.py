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

from dvc.core.struct import Operation, DatabaseVersion, DatabaseRevisionFile
from dvc.core.config import ConfigDefault, DatabaseRevisionFilesManager, ConfigReader, DatabaseConnectionFactory
from dvc.core.file import validate_file_exist
from dvc.core.exception import InvalidDatabaseRevisionFilesException, DatabaseConnectionFailureException, \
    OperationNotAccountedForException



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


    def execute_sql_files(self,
                          database_revision_files: List[DatabaseRevisionFile],
                          mark_only: bool = False,
                          ) -> None:

        database_revision_file = database_revision_files[0]

        if mark_only:
            logging.info(f"Now only marking {database_revision_file.file_path} to metadata table")
            self.sql_file_executor._write_database_revision_metadata(database_revision_file=database_revision_file)
        else:
            logging.info(f"Now applying {database_revision_file.file_path} and marking to metadata table")
            self.sql_file_executor.execute_database_revision(database_revision_file=database_revision_file)


    def get_target_database_revision_files(self,
                                           steps: Optional[int]
                                           ) -> List[Optional[DatabaseRevisionFile]]:
        """
        Helper to get target database revision file

        Check number of returned revision files must be same as steps specified

        :param operation_type: Specify the operation type
        :param steps: Specify how many steps ahead/ backwards.. When None, it goes to the very end in either direction
        :return:
        """
        # Step 1:
        if steps == 0:
            return []

        target_database_revision_files = self.database_revision_files_manager.get_target_database_revision_files_by_steps(
            current_database_version=self.latest_database_version,
            steps = steps,
        )


        return target_database_revision_files

    @property
    def latest_database_version(self) -> DatabaseVersion:
        latest_database_version: DatabaseVersion = self.sql_file_executor.get_latest_database_version()
        return latest_database_version

    @property
    def config_file_reader(self):
        if self.config_file_path is None:
            config_file_reader = ConfigReader(ConfigDefault.VAL__FILE_PATH)
        else:
            validate_file_exist(self.config_file_path)
            config_file_reader = ConfigReader(self.config_file_path)
        return config_file_reader

    @property
    def database_revision_files_manager(self):
        db_rv_files_man = DatabaseRevisionFilesManager(self.config_file_reader)
        return db_rv_files_man

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
