"""
Define the main commands of the CLI
"""
import logging
import traceback
from typing import List
from pathlib import Path
import typer

from dvc.core.database.postgres import SQLFileExecutor
from dvc.core.config import write_default_config_file, get_postgres_connection
from dvc.core.struct import DatabaseRevision, Operation, DatabaseVersion

from dvc.app.backend import get_target_database_revision_sql_files
from dvc.app.cli import config, database, sql

# Set default logging to INFO
logging.root.setLevel(logging.INFO)

app = typer.Typer()
app.add_typer(config.app, name='cfg', help="Config related subcommands")
app.add_typer(database.app, name='db', help="Database related subcommands")
app.add_typer(sql.app, name='sql', help="SQL files related subcommands")





