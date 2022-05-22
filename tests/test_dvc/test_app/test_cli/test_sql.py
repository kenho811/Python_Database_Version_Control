from typer.testing import CliRunner
from dvc.app.cli.config import app

import dvc.core.config
from dvc.core.config import write_default_config_file
from dvc.app.cli.config import init

runner = CliRunner()

