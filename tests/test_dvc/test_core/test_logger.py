import logging
from typing import Callable
import pytest

from dvc.core.logger import SetRootLoggingLevel
from dvc.core.config import ConfigDefault


@pytest.fixture
def any_func() -> Callable:
    """
    Return a function which accepts any args and kwargs, but does nothing
    :return:
    """

    def func(*args, **kwargs):
        pass

    return func


class TestSetRootLoggingLevel:
    """
    Test Set RootLoggingLevel as a decorator
    """

    def test__when_config_file_and_env_var_are_absent__set_to_default_logging_level(
            self,
            any_func,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_absent_config_file_path,
    ):
        """
        GIVEN config file is absent and no env var is set
        WHEN SetRootLoggingLevel is called
        THEN use default logging level

        :param any_func:
        :param dummy_user_configuration_with_supported_db_flavour:
        :param dummy_absent_config_file_path
        :return:
        """

        # Act
        SetRootLoggingLevel(any_func)(config_file_path=dummy_absent_config_file_path)

        # Assert
        assert logging.getLogger().getEffectiveLevel() == logging._nameToLevel[ConfigDefault.VAL__LOGGING_LEVEL]

    def test__when_config_file_is_absent_but_env_var_is_present__set_to_user_defined_logging_level(
            self,
            any_func,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_absent_config_file_path_with_env_var,
    ):
        """
        GIVEN config file is absent but env vars are set
        WHEN SetRootLoggingLevel is called
        THEN use the env vars' logging levels

        :param any_func:
        :param dummy_user_configuration_with_supported_db_flavour:
        :param dummy_absent_config_file_path_with_env_var
        :return:
        """

        # Act
        SetRootLoggingLevel(any_func)(config_file_path=dummy_absent_config_file_path_with_env_var)

        # Assert
        assert logging.getLogger().getEffectiveLevel() == dummy_user_configuration_with_supported_db_flavour['logging_level']

    def test__when_config_file_is_present_but_env_var_is_absent__set_to_config_file_logging_level(
            self,
            any_func,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_existing_config_file_path,
    ):
        """
        GIVEN config file is present and no env vars are set
        WHEN SetRootLoggingLevel is called
        THEN use the config file' logging level

        :param any_func:
        :param dummy_user_configuration_with_supported_db_flavour:
        :param dummy_existing_config_file_path:
        :return:
        """

        # Act
        SetRootLoggingLevel(any_func)(config_file_path=dummy_existing_config_file_path)

        # Assert
        assert logging.getLogger().getEffectiveLevel() == dummy_user_configuration_with_supported_db_flavour['logging_level']
