from typer.testing import CliRunner
from dvc.app.cli.config import app

from dvc.core.config import write_default_config_file


runner = CliRunner()


def test__cmd_init__call__func_write_default_config_file_once():
    from dvc.app.cli.config import init
    # mock_write_default_config_file = mocker.patch.object(write_default_config_file, 'do_time_consuming_task', autospec=True)  # Alt. B

    init()

    # mock_write_default_config_file.assert_has_calls([mocker.call(100), mocker.call(50)])
