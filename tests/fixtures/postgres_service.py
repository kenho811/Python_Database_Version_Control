import pytest
import psycopg2
from psycopg2._psycopg import connection


@pytest.fixture()
def pgconn(postgres_service) -> connection:
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
