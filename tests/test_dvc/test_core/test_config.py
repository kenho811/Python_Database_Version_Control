from unittest import mock
from unittest.mock import Mock, MagicMock, PropertyMock
import yaml
from typing import Dict
import pytest
import psycopg2
from pathlib import Path

import dvc.core.config

from dvc.core.config import DatabaseConnectionFactory, Default, ConfigFileWriter, ConfigFileReader
from dvc.core.exception import RequestedDatabaseFlavourNotSupportedException


class TestConfigFileWriter:
    def test__write_dummy_user_configuration(
            self,
            dummy_user_configuration_postgres_dict,
            tmp_path,
    ):
        """
        GIVEN a dummy config file with dummy user configuration,
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Arrange
        dummy_config_file_name: str = "another_dummy_config_file.yaml"
        dummy_config_file_path: Path = tmp_path.joinpath(dummy_config_file_name)

        # Action
        assert not dummy_config_file_path.is_file()

        # Action
        ConfigFileWriter(dummy_config_file_path).write_to_yaml()

        # Assert
        assert dummy_config_file_path.is_file()

        # TearDown
        dummy_config_file_path.unlink()


class TestConfigFileReader:
    def test__return_expected_user_config(
            self,
            dummy_user_configuration_postgres_dict,
            dummy_config_file_path: Path,
    ):
        """
        GIVEN a dummy config file with dummy user configuration,
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """

        # Action
        user_config = ConfigFileReader(dummy_config_file_path).user_config

        # Assert
        assert user_config == dummy_user_configuration_postgres_dict


class TestDatabaseRevisionFilesManager:

    def test__validate_database_revision_sql_files__raise_InvalidDatabaseRevisionFilesException_with_status_101(
            self,
            dummy_config_file_reader
    ):
        pass
        # assert False, dummy_config_file_reader.user_config


class TestDatabaseConnectionFactory:

    def test__raise_requested_database_not_supported_exception(
            self,
            dummy_user_configuration_postgres_dict,
    ):
        """
        GIVEN a fake database flavour
        WHEN DatabaseConnectionFactory.validate_requested_database_flavour is called
        THEN assert RequestedDatabaseFlavourNotSupportedException is raised
        """
        # Arrange
        requested_database_flavour = 'fake_database_flavour'

        with mock.patch('dvc.core.config.ConfigFileReader.requested_db_flavour',
                        new_callable=PropertyMock) as mock_requested_db_flavour:
            config_file_reader = ConfigFileReader()
            mock_requested_db_flavour.return_value = requested_database_flavour
            with pytest.raises(RequestedDatabaseFlavourNotSupportedException) as exc_info:
                DatabaseConnectionFactory(config_file_reader).validate_requested_database_flavour()

    def test__pass_user_credentials_to_connect_as_kwargs(
            self,
            dummy_user_configuration_postgres_dict,
    ):
        """
        GIVEN patched psycopg2.connect
        WHEN DatabaseConnectionFactory.conn is called
        THEN check psycopg2.connect is called once and with expected args
        """
        # Arrange
        with mock.patch('psycopg2.connect') as mock_connect:
            with mock.patch('dvc.core.config.ConfigFileReader.user_config',
                            new_callable=PropertyMock) as mock_user_config:
                # Arrange
                config_file_reader = ConfigFileReader()
                mock_user_config.return_value = dummy_user_configuration_postgres_dict
                # Act
                conn = DatabaseConnectionFactory(config_file_reader=config_file_reader).conn

                # Assert
                expects_args = {
                    "dbname": 'superman_db',
                    "user": 'peter_parker',
                    "password": '1234',
                    "port": 5432,
                    "host": 'localhost',
                }
                mock_connect.assert_called_once()
                mock_connect.assert_called_with(
                    **expects_args
                )
