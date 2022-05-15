"""
Define the main commands of the CLI
"""
import logging
import typer

from dvc.app.backend import get_target_database_revision_sql_files
from dvc import __version__
from dvc.app.cli import config, database, sql

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
