import psycopg2
from psycopg2._psycopg import connection
from pathlib import Path
from typing import Optional, Tuple

from dvc.core.database import SQLFileExecutorTemplate
from dvc.core.struct import DatabaseRevision, DatabaseVersion
from dvc.core.hash import FileHasher


class PostgresSQLFileExecutor(SQLFileExecutorTemplate):
    METADATA_SQL_FOLDER_PATH = Path(__file__).parent
    FILE_HASHER = FileHasher()

    def __init__(self,
                 conn: connection
                 ):
        self.conn = conn
        self.cur = self.conn.cursor()

    def set_up_database_revision_control_tables(self):
        """
        Create all database revision control schema and tables
        :return:
        """
        with open(self.__class__.METADATA_SQL_FOLDER_PATH.joinpath("scm_dvc__create_scm_and_tbls.sql"), 'r',
                  encoding='utf-8') as create_sql_file:
            create_sql = create_sql_file.read()
            self.cur.execute(query=create_sql)
            self.conn.commit()

    def get_latest_database_version(self) -> DatabaseVersion:
        """
        Get the latest database version
        :return:
        """
        sql_file_path = self.__class__.METADATA_SQL_FOLDER_PATH.joinpath("scm_dvc__select_latest_database_version.sql")
        with open(sql_file_path, 'r', encoding='utf-8') as select_latest_database_version_sql_file:
            select_latest_database_version_sql = select_latest_database_version_sql_file.read()

            self.cur.execute(query=select_latest_database_version_sql)

            result: Optional[Tuple] = self.cur.fetchone()

            if result is None:
                # Nothing is in the table
                latest_database_version: DatabaseVersion = DatabaseVersion(
                    current_version="V0",
                    next_upgrade_revision_version="RV1",
                    next_downgrade_revision_version=None,
                    created_at=None,
                )
            else:
                current_version, next_upgrade_revision_version, next_downgrade_revision_version, created_at = result
                latest_database_version: DatabaseVersion = DatabaseVersion(
                    current_version=current_version,
                    next_upgrade_revision_version=next_upgrade_revision_version,
                    next_downgrade_revision_version=next_downgrade_revision_version,
                    created_at=created_at
                )

        return latest_database_version

    def execute_database_revision(self,
                                  database_revision: DatabaseRevision
                                  ):
        """
        Execute database revision and write to database version control tables
        :param database_revision:
        :return:
        """
        with open(database_revision.executed_sql_file_path_applied, 'r', encoding='utf-8', ) as sql_file:
            sql = sql_file.read()
            self.cur.execute(sql)
            self.conn.commit()

        self._write_database_revision_metadata(database_revision=database_revision)

    def _write_database_revision_metadata(self,
                                          database_revision: DatabaseRevision
                                          ):
        """
        Write a given database revision to database version control tables
        :param database_revision:
        :return:
        """
        executed_sql_file_folder = str(database_revision.executed_sql_file_path_applied.parent)
        executed_sql_file_name = str(database_revision.executed_sql_file_path_applied.name)
        executed_sql_file_content_hash = self.__class__.FILE_HASHER.md5(database_revision.executed_sql_file_path_applied)
        with open(database_revision.executed_sql_file_path_applied, 'r', encoding='utf-8') as executed_sql_file:
            executed_sql_file_content = executed_sql_file.read()

        with open(self.__class__.METADATA_SQL_FOLDER_PATH.joinpath("scm_dvc__insert_tbl_database_revision_history.sql"),
                  'r', encoding='utf-8') as insert_sql_file:
            insert_sql = insert_sql_file.read()

            self.cur.execute(query=insert_sql,
                             vars=(executed_sql_file_folder,
                                   executed_sql_file_name,
                                   executed_sql_file_content_hash,
                                   executed_sql_file_content,
                                   database_revision.operation.name))
            self.conn.commit()
