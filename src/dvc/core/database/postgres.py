import psycopg2
from psycopg2._psycopg import connection
from pathlib import Path

from dvc.core.struct import SchemaRevision
from dvc.core.hash import md5
from dvc.core import METADATA_SQL_FOLDER_PATH


class SQLFileExecutor:

    def __init__(self,
                 conn: connection
                 ):
        self.conn = conn
        self.cur = self.conn.cursor()

    def execute_revision(self,
                         schema_revision: SchemaRevision
                         ):
        with open(schema_revision.executed_sql_file_path_applied, 'r') as sql_file:
            sql = sql_file.read()
            self.cur.execute(sql)
            self.conn.commit()

        self._create_audit_table()
        self._write_audit_table(revision=schema_revision)

    def _write_audit_table(self,
                           revision: SchemaRevision
                           ):
        executed_sql_file_folder = str(revision.executed_sql_file_path_applied.parent)
        executed_sql_file_name = str(revision.executed_sql_file_path_applied.name)
        executed_sql_file_content_hash = md5(revision.executed_sql_file_path_applied)

        with open(METADATA_SQL_FOLDER_PATH.joinpath("scm_dvc__insert_tbl_database_revision_history.sql"),
                  'r') as insert_sql_file:
            insert_sql = insert_sql_file.read()

            self.cur.execute(query=insert_sql,
                             vars=(executed_sql_file_folder, executed_sql_file_name, executed_sql_file_content_hash,
                                   revision.operation.name))
            self.conn.commit()

    def _create_audit_table(self):
        with open(METADATA_SQL_FOLDER_PATH.joinpath("scm_dvc__create_scm_and_tbls.sql"),
                  'r') as create_sql_file:
            create_sql = create_sql_file.read()
            self.cur.execute(query=create_sql)
            self.conn.commit()
