from unittest import mock
from unittest.mock import Mock
import yaml
from typing import Dict
import pytest
import psycopg2

import dvc.core.config

from dvc.core.config import DatabaseConnectionFactory, Default, ConfigFileWriter, ConfigFileReader


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


def test__DatabaseConnectionFactory__pass_user_credentials_to_connect_as_kwargs(
        monkeypatch,
        user_configuration_dict: Dict,
):
    """
    GIVEN a monkeypatched version of yaml.load
    WHEN read_config_file is called
    THEN check read_config_file returns the python dict from yaml.load
    """

    # Arrange
    mock_config_file_reader = Mock()
    mock_config_file_reader.user_config = user_configuration_dict

    with mock.patch('psycopg2.connect') as mock_connect:
        conn = DatabaseConnectionFactory(config_file_reader=mock_config_file_reader).pgconn
        mock_connect.assert_called_once()
        mock_connect.assert_called_with(dbname='superman_db', user='peter_parker', password='1234', port=5432, host='localhost')

