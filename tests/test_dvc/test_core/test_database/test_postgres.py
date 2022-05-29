import docker
import pytest
import requests
import psycopg2

from requests.exceptions import ConnectionError


def is_responsive(url):
    try:
        psycopg2.connect(url)
    except Exception as e:
        return False
    else:
        return True


@pytest.fixture(scope="session")
def postgres_service(docker_ip, docker_services):
    """Ensure that HTTP service is up and responsive."""

    # `port_for` takes a container port and returns the corresponding host port
    # docker_services.start('postgres_db')

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
    def test__connection(self,
                         postgres_service
                         ):
        assert False, f"URL is {postgres_service}"
