from unittest import mock
from unittest.mock import Mock, MagicMock
import yaml
from typing import Dict
import pytest
import psycopg2
from pathlib import Path

import dvc.core.config

from dvc.core.config import DatabaseConnectionFactory, Default, ConfigFileWriter, ConfigFileReader


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


@pytest.mark.usefixtures('init_dummy_config_file_path')
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


class TestDatabaseConnectionFactory:
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
        mock_config_file_reader = MagicMock(spec=ConfigFileReader)
        mock_config_file_reader.user_config = dummy_user_configuration_postgres_dict

        with mock.patch('psycopg2.connect') as mock_connect:
            # Act
            conn = DatabaseConnectionFactory(config_file_reader=mock_config_file_reader).conn

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
