import yaml
from typing import Dict
import pytest
import psycopg2._psycopg
from psycopg2._psycopg import connection, _connect

import dvc.core.config

from dvc.core.config import DatabaseConnectionFactory, Default, ConfigFileWriter, ConfigFileReader


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


def test__ConfigFileReader__return_expected_user_config(monkeypatch, user_configuration_dict: Dict):
    """
    GIVEN a monkeypatched version of yaml.load
    WHEN read_config_file is called
    THEN check read_config_file returns the python dict from yaml.load
    """

    def mock_load(*args, **kwargs) -> Dict:
        return user_configuration_dict

    # Arrange
    monkeypatch.setattr(yaml, "load", mock_load)

    # Action
    user_config = ConfigFileReader(Default.CONFIG_FILE_PATH).user_config

    # Assert
    assert user_config == user_configuration_dict


def test__DatabaseConnectionFactory__pass_user_credentials_to_connect_as_kwargs(monkeypatch, user_configuration_dict: Dict):
    """
    GIVEN a monkeypatched version of yaml.load
    WHEN read_config_file is called
    THEN check read_config_file returns the python dict from yaml.load
    """

    def mock_load(*args, **kwargs) -> Dict:
        return user_configuration_dict

    def mock_connect(*args, **kwargs):
        # Assert
        assert kwargs == {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
        }

    # Arrange
    monkeypatch.setattr(dvc.core.config.ConfigFileReader, "user_config", mock_load())
    monkeypatch.setattr(psycopg2, "connect", mock_connect)

    # Action
    conn = DatabaseConnectionFactory(config_file_path=Default.CONFIG_FILE_PATH).pgconn
    print(conn)

    # Assert
    assert conn.info.dbname == 'superman_db'
