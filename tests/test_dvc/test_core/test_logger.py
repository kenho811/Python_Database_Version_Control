from typing import Callable

import pytest


@pytest.fixture
def func_with_config_file_path_as_param(dummy_existing_config_file_path) -> Callable:
    def func(config_file_path=dummy_existing_config_file_path):
        pass
    return func


class TestSetRootLoggingLevel:
    """
    Test Set RootLoggingLevel as a decorator
    """

    def test_set_to_default_logging_level(self):
        pass

    def test_set_to_custom_logging_level(self):
        pass
