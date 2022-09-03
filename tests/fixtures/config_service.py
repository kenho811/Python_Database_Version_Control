import os

import pytest
from typing import Dict
from pathlib import Path
import yaml
import logging
from unittest import mock

# Import dvc
from dvc.core.config import ConfigReader, ConfigDefault
from dvc.core.database import SupportedDatabaseFlavour
import logging


@pytest.fixture(params=(logging.DEBUG, logging.WARNING, logging.CRITICAL, logging.ERROR))
def dummy_user_configuration_with_supported_db_flavour(request) -> Dict:
    """
    Fixture of User Configruration
    """
    DUMMY_USER_CONFIG: Dict = {
        "logging_level": request.param,
        "target_schema": 'dvc',
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
        "logging_level": logging.INFO,
        "target_schema": 'dvc',
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

@pytest.fixture
def dummy_absent_config_file_path_with_env_var(
        dummy_absent_config_file_path,
        dummy_user_configuration_with_supported_db_flavour,
        monkeypatch
):
    """
    Return path to a non-existing config file.
    Set environment variables additionally
    """
    # Set environment variables
    monkeypatch.setenv(ConfigDefault.KEY__DATABASE_REVISION_SQL_FILES_FOLDER, dummy_user_configuration_with_supported_db_flavour['database_revision_sql_files_folder'])
    monkeypatch.setenv(ConfigDefault.KEY__USER, dummy_user_configuration_with_supported_db_flavour['credentials']['user'])
    monkeypatch.setenv(ConfigDefault.KEY__PASSWORD, dummy_user_configuration_with_supported_db_flavour['credentials']['password'])
    monkeypatch.setenv(ConfigDefault.KEY__HOST, dummy_user_configuration_with_supported_db_flavour['credentials']['host'])
    monkeypatch.setenv(ConfigDefault.KEY__PORT, str(dummy_user_configuration_with_supported_db_flavour['credentials']['port']))
    monkeypatch.setenv(ConfigDefault.KEY__DBNAME, dummy_user_configuration_with_supported_db_flavour['credentials']['dbname'])
    monkeypatch.setenv(ConfigDefault.KEY__DBFLAVOUR, dummy_user_configuration_with_supported_db_flavour['credentials']['dbflavour'])
    monkeypatch.setenv(ConfigDefault.KEY__LOGGING_LEVEL, str(dummy_user_configuration_with_supported_db_flavour['logging_level']))
    yield dummy_absent_config_file_path


@pytest.fixture()
def dummy_config_file_reader_with_supported_db_flavour(
        dummy_user_configuration_with_supported_db_flavour
):
    """
    Yield dummy config file reader with user_config property patched
    """

    with mock.patch('dvc.core.config.ConfigReader') as mock_cls:
        mock_config_reader = mock_cls.return_value
        mock_config_reader.user_config = dummy_user_configuration_with_supported_db_flavour
        mock_config_reader.requested_db_flavour = dummy_user_configuration_with_supported_db_flavour['credentials'][
            'dbflavour']

        yield mock_config_reader


@pytest.fixture()
def dummy_config_file_reader_with_unsupported_db_flavour(
        dummy_user_configuration_with_unsupported_db_flavour
):
    """
    Yield dummy config file reader with user_config property patched
    """

    with mock.patch('dvc.core.config.ConfigReader') as mock_cls:
        mock_config_reader = mock_cls.return_value
        mock_config_reader.user_config = dummy_user_configuration_with_unsupported_db_flavour
        mock_config_reader.requested_db_flavour = dummy_user_configuration_with_unsupported_db_flavour['credentials'][
            'dbflavour']

        yield mock_config_reader
