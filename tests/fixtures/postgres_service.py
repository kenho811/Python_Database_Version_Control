from unittest import mock
import pytest
import psycopg2
from psycopg2._psycopg import connection


@pytest.fixture()
def dummy_pgconn() -> mock.MagicMock:
    """
    Return a dummy pgconn
    """
    # Set up
    with mock.patch('psycopg2.connect') as mock_connect:
        yield mock_connect

    # Tear down


@pytest.fixture()
def real_pgconn(postgres_service) -> connection:
    """
    Return a real pgconn (connected to a real postgres container)
    """
    return psycopg2.connect(postgres_service)


@pytest.fixture(scope="class")
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
