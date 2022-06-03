import docker
import pytest
import requests
import psycopg2
from psycopg2._psycopg import connection

from dvc.core.database.postgres import PostgresSQLFileExecutor
from dvc.core.struct import DatabaseVersion, DatabaseRevision, Operation


from requests.exceptions import ConnectionError


@pytest.mark.integration
@pytest.mark.usefixtures('postgres_service')
class TestSQLFileExecutor:
    """
    Integration tests with Postgresql
    """

    @pytest.fixture()
    def postgres_sql_file_executor(self,
                                   real_pgconn
                                   ):
        # Arrange
        postgres_sql_file_executor = PostgresSQLFileExecutor(real_pgconn)
        postgres_sql_file_executor.set_up_database_revision_control_tables()
        return postgres_sql_file_executor

    def test__assert_database_version_zero(
            self,
            postgres_sql_file_executor,
    ):
        # Assert
        dv = postgres_sql_file_executor.get_latest_database_version()
        assert dv == DatabaseVersion(current_version='V0',
                                     next_downgrade_revision_version=None,
                                     next_upgrade_revision_version='RV1',
                                     created_at=None
                                     )

    def test__when_rv1_upgrade_revisions_applied__assert_2_new_tables_in_schema_fundamentals(
            self,
            real_pgconn,
            postgres_sql_file_executor,
            rv1_upgrade_database_revision,
    ):
        # Arrange
        dv = postgres_sql_file_executor.execute_database_revision(rv1_upgrade_database_revision)

        # Assert 2 tables in sceham fundamentals
        sql = f"""
        select count(*) from information_schema.tables where table_schema = 'fundamentals';
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 2

        # Assert one row in dvc.database_revision_history
        sql = f"""
        select count(*) from dvc.database_revision_history;
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result
        assert cnt == 1


    def test__when_rv2_upgrade_revisions_applied__assert_1_new_tables_in_schema_datetime(
            self,
            real_pgconn,
            postgres_sql_file_executor,
            rv2_upgrade_database_revision,
    ):
        # Arrange
        dv = postgres_sql_file_executor.execute_database_revision(rv2_upgrade_database_revision)

        # Assert 1 table in schema datetime
        sql = f"""
        select count(*) from information_schema.tables where table_schema = 'datetime';
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 1

        # Assert 2 rows in dvc.database_revision_history
        sql = f"""
        select count(*) from dvc.database_revision_history;
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 2

    def test__when_rv2_downgrade_revisions_applied__assert_0_new_tables_in_schema_datetime(
            self,
            real_pgconn,
            postgres_sql_file_executor,
            rv2_downgrade_database_revision,
    ):
        # Arrange
        dv = postgres_sql_file_executor.execute_database_revision(rv2_downgrade_database_revision)

        # Assert 1 table in schema datetime
        sql = f"""
        select count(*) from information_schema.tables where table_schema = 'datetime';
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 0

        # Assert 2 rows in dvc.database_revision_history
        sql = f"""
        select count(*) from dvc.database_revision_history;
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 3

    def test__when_rv1_downgrade_revisions_applied__assert_0_new_tables_in_schema_fundamentals(
            self,
            real_pgconn,
            postgres_sql_file_executor,
            rv1_downgrade_database_revision,
    ):
        # Arrange
        dv = postgres_sql_file_executor.execute_database_revision(rv1_downgrade_database_revision)

        # Assert 1 table in schema datetime
        sql = f"""
        select count(*) from information_schema.tables where table_schema = 'fundamentals';
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 0

        # Assert 2 rows in dvc.database_revision_history
        sql = f"""
        select count(*) from dvc.database_revision_history;
        """
        cur = real_pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 4
