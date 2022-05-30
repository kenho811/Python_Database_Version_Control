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
        user_config = ConfigFileReader(dummy_existing_config_file_path).user_config

        # Assert
        assert user_config == dummy_user_configuration_with_supported_db_flavour


class TestDatabaseRevisionFilesManager:

    def test__validate_database_revision_sql_files__raise_InvalidDatabaseRevisionFilesException_with_status_101(
            self,
            dummy_config_file_reader_with_supported_db_flavour
    ):
        pass
        # assert False, dummy_config_file_reader.user_config


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
