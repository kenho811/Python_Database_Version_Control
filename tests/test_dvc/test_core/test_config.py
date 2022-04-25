import yaml
from typing import Dict
import pytest
import psycopg2._psycopg
from psycopg2._psycopg import connection, _connect

import dvc.core.config

from dvc.core.config import read_config_file, get_postgres_connection


@pytest.fixture
def user_configuration_dict() -> Dict:
    """
    Fixture of User Configruration
    """
    USER_CONFIG_FILE: Dict = {
        "database_revision_sql_files_folder": "sample_revision_sql_files",
        "credentials": {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
        }
    }
    return USER_CONFIG_FILE


def test__read_config_file__return_expected_user_config(monkeypatch, user_configuration_dict):
    """
    GIVEN a monkeypatched version of yaml.load
    WHEN read_config_file is called
    THEN check read_config_file returns the python dict from yaml.load
    """

    def mock_load(*args, **kwargs) -> Dict:
        return user_configuration_dict

    monkeypatch.setattr(yaml, "load", mock_load)
    assert read_config_file() == {
        "database_revision_sql_files_folder": "sample_revision_sql_files",
        "credentials": {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
        }
    }


def test__get_postgres_connection__pass_user_credentials_to_connect_as_kwargs(monkeypatch, user_configuration_dict):
    """
    GIVEN a monkeypatched version of yaml.load
    WHEN read_config_file is called
    THEN check read_config_file returns the python dict from yaml.load
    """

    def mock_load(*args, **kwargs) -> Dict:
        return user_configuration_dict

    def mock_connect(*args, **kwargs):
        assert kwargs == {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
        }

    monkeypatch.setattr(dvc.core.config, "read_config_file", mock_load)
    monkeypatch.setattr(psycopg2, "connect", mock_connect)

    get_postgres_connection()
