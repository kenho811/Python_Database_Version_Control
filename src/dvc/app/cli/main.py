'''
Starting point of the CLI
'''
"""
Define the main commands of the CLI
"""
import logging
import typer

from dvc.version import __version__
from dvc.app.cli.commands import config, database
from dvc.core.logger import SetRootLoggingLevel
from dvc.core.config import ConfigDefault

DOCUMENTATION_URL = "https://python-database-version-control.readthedocs.io/en/latest/"
EPILOG_TXT = f"Doc: {DOCUMENTATION_URL}"
HELP_TXT = "A Database Version Control Tool"

app = typer.Typer(
    help=HELP_TXT,
    short_help=HELP_TXT,
    epilog=EPILOG_TXT,
)
app.add_typer(config.app, name='cfg', help="Config related subcommands")
app.add_typer(database.app, name='db', help="Database related subcommands")


@app.command()
@SetRootLoggingLevel
def version(
        config_file_path: str = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
):
    """
    Show CLI version
    """
    typer.echo(__version__)


if __name__ == "__main__":
    app()
