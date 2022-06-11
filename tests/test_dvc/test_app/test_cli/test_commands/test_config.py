import pytest
from typer.testing import CliRunner

from dvc.app.cli.commands.config import app

runner = CliRunner()


@pytest.mark.unit
def test__init__no_error_when_called_twice():
    """
    Test no error when called twice
    """
    result_1 = runner.invoke(app)
    assert result_1.exit_code == 0

    result_2 = runner.invoke(app)
    assert result_2.exit_code == 0
