from typer.testing import CliRunner
from unittest.mock import Mock

import dvc.core.config
from dvc.app.cli.config import init
from dvc.app.cli.config import app

runner = CliRunner()


def test__init__call_func_write_default_config_file_once(monkeypatch):
    """
    Test Behaviour of init() func
    """
    counter = 0

    mock_write_default_config_file = Mock()
    mock_generate_database_revision_sql_folder = Mock()

    # Arrange
    monkeypatch.setattr(dvc.app.cli.config, 'write_default_config_file', mock_write_default_config_file)
    monkeypatch.setattr(dvc.app.cli.config, 'generate_database_revision_sql_folder',
                        mock_generate_database_revision_sql_folder)

    # Act
    init()

    # Assert
    mock_write_default_config_file.assert_called_once()
    mock_generate_database_revision_sql_folder.assert_called_once()


def test__init__no_error_when_called_twice():
    """
    Test no error when called twice
    """
    result_1 = runner.invoke(app)
    assert result_1.exit_code == 0

    result_2 = runner.invoke(app)
    assert result_2.exit_code == 0
