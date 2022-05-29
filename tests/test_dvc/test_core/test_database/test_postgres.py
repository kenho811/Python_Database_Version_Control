import docker
import pytest
import requests
import psycopg2
from psycopg2._psycopg import connection

from dvc.core.database.postgres import PostgresSQLFileExecutor
from dvc.core.struct import DatabaseVersion, DatabaseRevision, Operation


from requests.exceptions import ConnectionError


@pytest.fixture()
def pgconn(postgres_service) -> connection:
    return psycopg2.connect(postgres_service)


@pytest.fixture(scope="session")
def postgres_service(docker_ip, docker_services):
    """Ensure that Postgres service is up and responsive."""

    def is_responsive(url):
        try:
            psycopg2.connect(url)
        except Exception as e:
            return False
        else:
            return True

    port = docker_services.port_for("postgres_db", 5432)
    username = 'test'
    password = 'test'
    db = 'test'
    url = f"postgresql://{username}:{password}@{docker_ip}:{port}/{db}"
    docker_services.wait_until_responsive(
        timeout=30.0, pause=0.1, check=lambda: is_responsive(url)
    )
    return url




@pytest.mark.usefixtures('postgres_service')
class TestSQLFileExecutor:
    """
    Integration tests with Postgresql
    """

    @pytest.fixture()
    def postgres_sql_file_executor(self,
                                   pgconn
                                   ):
        # Arrange
        postgres_sql_file_executor = PostgresSQLFileExecutor(pgconn)
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
            pgconn,
            postgres_sql_file_executor,
            rv1_upgrade_database_revision,
    ):
        # Arrange
        dv = postgres_sql_file_executor.execute_database_revision(rv1_upgrade_database_revision)

        # Assert 2 tables in sceham fundamentals
        sql = f"""
        select count(*) from information_schema.tables where table_schema = 'fundamentals';
        """
        cur = pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 2

        # Assert one row in dvc.database_revision_history
        sql = f"""
        select count(*) from dvc.database_revision_history;
        """
        cur = pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result
        assert cnt == 1

    def test__when_rv2_upgrade_revisions_applied__assert_1_new_tables_in_schema_datetime(
            self,
            pgconn,
            postgres_sql_file_executor,
            rv2_upgrade_database_revision,
    ):
        # Arrange
        dv = postgres_sql_file_executor.execute_database_revision(rv2_upgrade_database_revision)

        # Assert 1 table in schema datetime
        sql = f"""
        select count(*) from information_schema.tables where table_schema = 'datetime';
        """
        cur = pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 1

        # Assert 2 rows in dvc.database_revision_history
        sql = f"""
        select count(*) from dvc.database_revision_history;
        """
        cur = pgconn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        cnt, = result

        assert cnt == 2