import pytest
from typer.testing import CliRunner
import re

from dvc.app.cli.main import app

runner = CliRunner()


@pytest.mark.unit
def test__version__only_contain_semver():
    """
    Test `dvc version` command output version in SemVer format
    """
    result_1 = runner.invoke(app, ['version'])
    assert result_1.exit_code == 0

    version = result_1.output
    semver_regex = r"[0-9]+\.[0-9]+\.[0-9]+"
    match = re.search(semver_regex, version)

    assert match is not None, version
