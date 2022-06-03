import pytest
from typing import Dict
from pathlib import Path
import yaml
import logging
from unittest import mock

# Import dvc
from dvc.core.config import ConfigReader, ConfigDefault
from dvc.core.database import SupportedDatabaseFlavour



@pytest.fixture()
def dummy_user_configuration_with_supported_db_flavour() -> Dict:
    """
    Fixture of User Configruration
    """
    DUMMY_USER_CONFIG: Dict = {
        "database_revision_sql_files_folder": "sample_revision_sql_files",
        "credentials": {
            "user": "peter_parker",
            "password": "1234",
            "host": "localhost",
            "port": 5432,
            "dbname": "superman_db",
            "dbflavour": SupportedDatabaseFlavour.Postgres.value
        }
    }
    return DUMMY_USER_CONFIG


@pytest.fixture()
def dummy_user_configuration_with_unsupported_db_flavour() -> Dict:
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
            "dbflavour": "UNSUPPORTED DATABASE FLAVOUR!!!!!"
        }
    }
    return DUMMY_USER_CONFIG_FILE


@pytest.fixture
def dummy_existing_config_file_path(
        tmp_path,
        dummy_user_configuration_with_supported_db_flavour):
    """
    Set up the dummy config file
    Yield the dummy config file path
    Delete the dummy config file afterwards
    """
    dummy_existing_config_file_path = tmp_path.joinpath('dummy_existing_config_file_path.yaml')
    # Set up
    with open(dummy_existing_config_file_path, 'w') as dummy_config_file:
        logging.info(f"creating file {dummy_existing_config_file_path}")
        yaml.dump(dummy_user_configuration_with_supported_db_flavour, dummy_config_file, default_flow_style=False)
        yield dummy_existing_config_file_path

    # Tear down
    logging.info(f"deleting file {dummy_existing_config_file_path}")
    dummy_existing_config_file_path.unlink()


@pytest.fixture
def dummy_absent_config_file_path(
        tmp_path,
        dummy_user_configuration_with_supported_db_flavour,
        monkeypatch
):
    """
    Return path to a non-existing config file
    """
    dummy_absent_config_file_path = tmp_path.joinpath('dummy_absent_config_file_path.yaml')

    # Set up:
    # Step 1: Remove the file if it exists
    if dummy_absent_config_file_path.is_file():
        logging.info(f"File {dummy_absent_config_file_path} is found. Deleting...")
        dummy_absent_config_file_path.unlink()


    yield dummy_absent_config_file_path

    # Tear down:
    # Step 1: Remove the file if it exists
    if dummy_absent_config_file_path.is_file():
        logging.info(f"File {dummy_absent_config_file_path} is found. Deleting...")
        dummy_absent_config_file_path.unlink()



@pytest.fixture()
def dummy_config_file_reader_with_supported_db_flavour(
        dummy_user_configuration_with_supported_db_flavour
):
    """
    Yield dummy config file reader with user_config property patched
    """

    with mock.patch('dvc.core.config.ConfigReader.user_config',
                    new_callable=mock.PropertyMock,
                    return_value=dummy_user_configuration_with_supported_db_flavour) as mock_user_config:
        yield ConfigReader()


@pytest.fixture()
def dummy_config_file_reader_with_unsupported_db_flavour(
        dummy_user_configuration_with_unsupported_db_flavour
):
    """
    Yield dummy config file reader with user_config property patched
    """

    with mock.patch('dvc.core.config.ConfigReader.user_config',
                    new_callable=mock.PropertyMock,
                    return_value=dummy_user_configuration_with_unsupported_db_flavour) as mock_user_config:
        yield ConfigReader()