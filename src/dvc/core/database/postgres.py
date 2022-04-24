import psycopg2
from psycopg2._psycopg import connection
from pathlib import Path

from dvc.core.struct import Revision
from dvc.core.hash import md5
from dvc.core import METADATA_SQL_FOLDER_PATH


class SQLFileExecutor:

    def __init__(self,
                 conn: connection
                 ):
        self.conn = conn
        self.cur = self.conn.cursor()

    def execute_revision(self,
                         revision: Revision
                         ):
        with open(revision.sql_file_path, 'r') as sql_file:
            sql = sql_file.read()
            self.cur.execute(sql)
            self.conn.commit()

        self._create_audit_table()
        self._write_audit_table(revision=revision)

    def _write_audit_table(self,
                           revision: Revision
                           ):
        executed_sql_file_name = revision.sql_file_path.name
        executed_sql_file_hash = md5(revision.sql_file_path)

        with open(METADATA_SQL_FOLDER_PATH.joinpath("scm_public__insert_tbl_schema_revision_history.sql"),
                  'r') as insert_sql_file:
            insert_sql = insert_sql_file.read()

            self.cur.execute(query=insert_sql,
                             vars=(executed_sql_file_name, executed_sql_file_hash, revision.operation.name))
            self.conn.commit()

    def _create_audit_table(self):
        with open(METADATA_SQL_FOLDER_PATH.joinpath("scm_public__create_tbl_schema_revision_history.sql"),
                  'r') as create_sql_file:
            create_sql = create_sql_file.read()
            self.cur.execute(query=create_sql)
            self.conn.commit()
