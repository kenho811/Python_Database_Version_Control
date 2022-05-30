import pytest
from typing import Dict
from pathlib import Path
import yaml
import logging
from unittest import mock

# Import dvc
from dvc.core.config import ConfigFileReader


@pytest.fixture()
def dummy_user_configuration_postgres_dict() -> Dict:
    """
    Fixture of User Configruration
    """
    DUMMY_USER_CONFIG_FILE: Dict = {
        "database_revision_sql_files_folder": "sample_revision_sql_files",
        "credentials": {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
            "dbflavour": "postgres"
        }
    }
    return DUMMY_USER_CONFIG_FILE


@pytest.fixture
def dummy_config_file_path(
        tmp_path,
        dummy_user_configuration_postgres_dict):
    """
    Set up the dummy config file
    Yield the dummy config file path
    Delete the dummy config file afterwards
    """
    dummy_config_file_path = tmp_path.joinpath('dummy_config_file_path.yaml')
    # Set up
    with open(dummy_config_file_path, 'w') as dummy_config_file:
        logging.info(f"creating file {dummy_config_file_path}")
        yaml.dump(dummy_user_configuration_postgres_dict, dummy_config_file, default_flow_style=False)
        yield dummy_config_file_path

    # Tear down
    logging.info(f"deleting file {dummy_config_file_path}")
    dummy_config_file_path.unlink()


@pytest.fixture()
def dummy_config_file_reader(
        dummy_user_configuration_postgres_dict
):
    """
    Yield dummy config file reader with user_config property patched
    """

    with mock.patch('dvc.core.config.ConfigFileReader.user_config',
                    new_callable=mock.PropertyMock,
                    return_value=dummy_user_configuration_postgres_dict) as mock_user_config:
        yield ConfigFileReader()
