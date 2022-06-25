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

    def test_set_to_default_logging_level(self,
                                         any_func,
                                         dummy_user_configuration_with_supported_db_flavour,
                                         dummy_absent_config_file_path,
                                         ):
        """
        Does not pass config_file_path to SetRootLoggingLevel decorator.
        Expect setting rootlogginglevel to default

        :param any_func:
        :param dummy_user_configuration_with_supported_db_flavour:
        :param dummy_existing_config_file_path:
        :return:
        """

        # Act
        SetRootLoggingLevel(any_func)(dummy_absent_config_file_path)

        # Assert
        assert logging.getLogger().getEffectiveLevel() == logging._nameToLevel[ConfigDefault.VAL__LOGGING_LEVEL]

    def test_set_to_custom_logging_level(self,
                                         any_func,
                                         dummy_user_configuration_with_supported_db_flavour,
                                         dummy_existing_config_file_path,
                                         ):
        """
        Does not pass config_file_path to SetRootLoggingLevel decorator.
        Expect setting rootlogginglevel to default

        :param any_func:
        :param dummy_user_configuration_with_supported_db_flavour:
        :param dummy_existing_config_file_path:
        :return:
        """


        # Act
        SetRootLoggingLevel(any_func)(config_file_path=dummy_existing_config_file_path)

        # Assert
        assert logging.getLogger().getEffectiveLevel() == dummy_user_configuration_with_supported_db_flavour['logging_level']
