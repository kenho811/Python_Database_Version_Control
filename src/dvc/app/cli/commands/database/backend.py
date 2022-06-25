import traceback
from typing import Optional, List
from pathlib import Path
import re
import logging
from psycopg2._psycopg import connection

from dvc.core.database import SupportedDatabaseFlavour

from dvc.core.database.postgres import PostgresSQLFileExecutor

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
                 config_file_path_str: str,
                 ) -> None:
        """

        :param config_file_path_str: String pointing to the path where configuration file is located
        """
        self.config_file_path: Path = Path(config_file_path_str)

        if not (self.config_file_path.is_file() and self.config_file_path.exists()):
            # Use default
            self.config_file_reader = ConfigReader(ConfigDefault.VAL__FILE_PATH)
        else:
            self.config_file_reader = ConfigReader(self.config_file_path)

    def ping(self) -> None:
        """
        Ping the database connection

        :return:
        """
        try:
            conn = self.conn
        except Exception as e:
            logging.error(traceback.format_exc())
            raise DatabaseConnectionFailureException
        else:
            logging.info("Database connection looks good!")

    def execute_single_sql_file(self,
                                database_revision_file: DatabaseRevisionFile,
                                mark_only: bool = False,
                                ) -> None:
        """
        Execute DatabaseRevisionFile to the Database and optionally mark it as metadata

        :param database_revision_file: Database Revision File to apply to the Database
        :param mark_only: whether or not to mark the SQL file as being done as metadata, without actually executing the SQL file
        :return:
        """

        if mark_only:
            logging.info(f"Now only marking {database_revision_file.file_path} to metadata table")
            self.sql_file_executor._write_database_revision_metadata(database_revision_file=database_revision_file)
        else:
            logging.info(f"Now applying {database_revision_file.file_path} and marking to metadata table")
            self.sql_file_executor.execute_database_revision(database_revision_file=database_revision_file)

    def get_target_database_revision_files(self,
                                           steps: int,
                                           pointer: Optional[DatabaseRevisionFilesManager.Pointer] = None,
                                           ) -> List[DatabaseRevisionFile]:
        """
        Helper to get target database revision files
        Check number of returned revision files must be same as steps specified

        :param steps: Specify how many steps ahead/ backwards.. When None, it goes to the very end in either direction
        :return: List of DatabaseRevisionFiles, if any
        """
        # Step 1:
        if steps == 0:
            return []

        # Step 1: Get all database revision files
        all_database_revision_files = self.database_revision_files_manager.all_database_revision_files

        if pointer is not None:
            # Use pointer
            target_database_revision_files = self.database_revision_files_manager.get_target_database_revision_files_by_pointer(
                current_database_version=self.latest_database_version,
                pointer=pointer,
                candidate_database_revision_files=all_database_revision_files,
            )
        else:
        # Use steps
            # Filter for target revision files
            target_database_revision_files = self.database_revision_files_manager.get_target_database_revision_files_by_steps(
                current_database_version=self.latest_database_version,
                steps=steps,
                candidate_database_revision_files=all_database_revision_files,
            )

        return target_database_revision_files

    @property
    def latest_database_version(self) -> DatabaseVersion:
        """
        :return: latest Database Version
        """
        latest_database_version: DatabaseVersion = self.sql_file_executor.get_latest_database_version()
        return latest_database_version

    @property
    def database_revision_files_manager(self) -> DatabaseRevisionFilesManager:
        """

        :return:  DatabaseRevisionFilesManager
        """
        db_rv_files_man = DatabaseRevisionFilesManager(self.config_file_reader)
        return db_rv_files_man

    @property
    def conn(self):
        """

        :return:
        """
        config_file_reader = self.config_file_reader
        conn = DatabaseConnectionFactory(config_reader=config_file_reader).conn
        return conn

    @property
    def sql_file_executor(self):
        config_file_reader = self.config_file_reader
        conn = self.conn
        supported_db_flavour = DatabaseConnectionFactory(
            config_reader=config_file_reader).validate_requested_database_flavour()
        sql_file_executor = self.__class__.MAPPING[supported_db_flavour](conn)
        return sql_file_executor
