from typer.testing import CliRunner
from dvc.app.cli.config import app

import dvc.core.config
from dvc.core.config import write_default_config_file
from dvc.app.cli.config import init

runner = CliRunner()


def test__init__call_func_write_default_config_file_once(monkeypatch):
    counter = 0

    def mock_write_default_config_file():
        nonlocal counter
        counter += 1

    # Arrange
    monkeypatch.setattr(dvc.app.cli.config, 'write_default_config_file', mock_write_default_config_file)

    # Act
    init()

    # Assert
    assert counter == 1

