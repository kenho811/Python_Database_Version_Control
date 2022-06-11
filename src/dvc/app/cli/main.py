'''
Starting point of the CLI
'''
"""
Define the main commands of the CLI
"""
import logging
import typer

from dvc.version import __version__
from dvc.app.cli.commands import config, database, sql

# Set default logging to INFO
logging.root.setLevel(logging.INFO)

app = typer.Typer()
app.add_typer(config.app, name='cfg', help="Config related subcommands")
app.add_typer(database.app, name='db', help="Database related subcommands")
app.add_typer(sql.app, name='sql', help="SQL files related subcommands")


@app.command()
def version():
    """
    Show CLI version
    """
    typer.echo(__version__)


if __name__ == "__main__":
    app()
