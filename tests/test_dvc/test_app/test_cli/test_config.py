import pytest
from typing import Dict
from typer.testing import CliRunner
from unittest.mock import Mock, patch

import dvc.core.config
from dvc.app.cli.config import init
from dvc.app.cli.config import app

runner = CliRunner()


def test__init__call_func_write_default_config_file_once(monkeypatch,
                                                         user_configuration_dict,
                                                         ):
    """
    Test Behaviour of init() func
    """

    with patch("dvc.app.cli.config.ConfigFileWriter") as mock_config_file_writer:
        init()
        mock_config_file_writer.assert_called_once()


def test__init__no_error_when_called_twice():
    """
    Test no error when called twice
    """
    result_1 = runner.invoke(app)
    assert result_1.exit_code == 0

    result_2 = runner.invoke(app)
    assert result_2.exit_code == 0
