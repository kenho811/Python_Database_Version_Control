from unittest import mock
from unittest.mock import Mock, MagicMock, PropertyMock
import yaml
from typing import Dict
import pytest
import psycopg2
from pathlib import Path

import dvc.core.config

from dvc.core.config import DatabaseConnectionFactory, ConfigDefault, ConfigFileWriter, ConfigReader, \
    DatabaseRevisionFilesManager
from dvc.core.exception import RequestedDatabaseFlavourNotSupportedException, InvalidDatabaseRevisionFilesException


class TestConfigFileWriter:

    def test__write_dummy_user_configuration(
            self,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_absent_config_file_path,
    ):
        """
        GIVEN a non-existing config file path
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Action
        ConfigFileWriter(dummy_absent_config_file_path).write_to_yaml()

        # Assert
        assert dummy_absent_config_file_path.is_file()


class TestConfigFileReader:
    def test__return_expected_user_config(
            self,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_existing_config_file_path,
    ):
        """
        GIVEN a dummy config file with dummy user configuration,
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Action
        user_config = ConfigReader(dummy_existing_config_file_path).user_config

        # Assert
        assert user_config == dummy_user_configuration_with_supported_db_flavour


class TestDatabaseRevisionFilesManager:

    @pytest.fixture()
    def dummy_config_file_reader_with_patched_database_revision_files_folder(
            self,
            dummy_regex_files_folder_with_incorrect_files_names
    ):
        """
        Yield a config file reader which points to a regex files folder with incorrect files names
        """
        # Arrange
        with mock.patch('dvc.core.config.ConfigReader.user_config',
                        new_callable=mock.PropertyMock,
                        return_value={
                            "database_revision_sql_files_folder": dummy_regex_files_folder_with_incorrect_files_names}) as mock_user_config:
            yield ConfigReader()

    def test__validate_database_revision_sql_files__raise_InvalidDatabaseRevisionFilesException_with_status_101(
            self,
            dummy_config_file_reader_with_patched_database_revision_files_folder,
    ):
        db_rev_man = DatabaseRevisionFilesManager(
            dummy_config_file_reader_with_patched_database_revision_files_folder)
        with pytest.raises(InvalidDatabaseRevisionFilesException) as exc_info:
            db_rev_man.validate_database_revision_sql_files()




class TestDatabaseConnectionFactory:

    def test__raise_requested_database_not_supported_exception(
            self,
            dummy_config_file_reader_with_unsupported_db_flavour,
    ):
        """
        GIVEN a fake database flavour
        WHEN DatabaseConnectionFactory.validate_requested_database_flavour is called
        THEN assert RequestedDatabaseFlavourNotSupportedException is raised
        """
        # Assert
        with pytest.raises(RequestedDatabaseFlavourNotSupportedException) as exc_info:
            # Act
            DatabaseConnectionFactory(
                dummy_config_file_reader_with_unsupported_db_flavour).validate_requested_database_flavour()

    def test__pass_user_credentials_to_connect_as_kwargs(
            self,
            dummy_config_file_reader_with_supported_db_flavour,
            dummy_pgconn,
    ):
        """
        (Currently test postgres specifically)
        GIVEN patched psycopg2.connect
        WHEN DatabaseConnectionFactory.conn is called
        THEN check psycopg2.connect is called once and with expected args
        """
        # Act
        DatabaseConnectionFactory(config_file_reader=dummy_config_file_reader_with_supported_db_flavour).conn

        # Assert
        expects_args = {
            "dbname": 'superman_db',
            "user": 'peter_parker',
            "password": '1234',
            "port": 5432,
            "host": 'localhost',
        }
        dummy_pgconn.assert_called_once()
        dummy_pgconn.assert_called_with(
            **expects_args
        )
