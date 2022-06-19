"""
database subcommand
"""

import logging
from typing import List, Optional
from pathlib import Path
import typer

from dvc.core.struct import DatabaseRevisionFile, Operation, DatabaseVersion

from dvc.app.cli.commands.database.backend import DatabaseInteractor

app = typer.Typer()


@app.command()
def init(
        config_file_path: Optional[str] = typer.Option(None, help="path to config file"),
):
    """
    Generate configuration template & Initialise database
    """
    # Step 2: Set up metadata schema and tables
    db_interactor = DatabaseInteractor(config_file_path)
    conn = db_interactor.conn
    sql_file_executor = db_interactor.sql_file_executor
    sql_file_executor.set_up_database_revision_control_tables()

    typer.echo("Database init successful!")
    typer.echo(f"Database: {conn.info.dbname}")
    typer.echo(f"Host: {conn.info.host}")


@app.command()
def upgrade(
        config_file_path: Optional[str] = typer.Option(None, help="path to config file"),
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying'),
        confirm: bool = typer.Option(True, help='Prompt user to confirm operation or not.'),
):
    """
    Upgrade the Current Database Version by applying a corresponding Upgrade Revision Version
    """
    # Step 1: Check latest database version
    steps = 1
    operation_type = Operation.Upgrade
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version

    typer.echo(f"Current Database Version is {latest_database_version.version}")
    typer.echo(f"Next Upgrade Revision Version will be {latest_database_version.next_upgrade_database_revision_file.revision_number}")

    target_database_revision_files = db_interactor.get_target_database_revision_files(steps=1)

    if confirm:
        logging.info(f"Going to apply file {target_database_revision_files[0]} .....")
        resp = typer.confirm("You sure you want to continue ?")
        if not resp:
            raise typer.Abort()

    db_interactor.execute_sql_files(mark_only=mark_only,
                                    database_revision_files=target_database_revision_files)



@app.command()
def downgrade(
        config_file_path: Optional[str] = typer.Option(None, help="path to config file"),
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying'),
        confirm: bool = typer.Option(True, help='Prompt user to confirm operation or not.'),
):
    """
    Downgrade the Current Database Version by applying a corresponding Downgrade Revision Version
    :return:
    """
    # Step 1: Check latest database version
    steps = -1
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version

    typer.echo(f"Current Database Version is {latest_database_version.version}")
    typer.echo(f"Next Downgrade Revision Version will be {latest_database_version.next_downgrade_database_revision_file.revision_number}")

    target_database_revision_files = db_interactor.get_target_database_revision_files(steps=-1)

    if confirm:
        logging.info(f"Going to apply file {target_database_revision_files[0]} .....")
        resp = typer.confirm("You sure you want to continue ?")
        if not resp:
            raise typer.Abort()

    db_interactor.execute_sql_files(mark_only=mark_only,
                                    database_revision_files=target_database_revision_files)


@app.command()
def current(config_file_path: Optional[str] = typer.Option(None, help="path to config file")):
    """
    Check the current Database Version
    :return:
    """
    db_interactor = DatabaseInteractor(config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version
    typer.echo(f"Database Current Version: {latest_database_version.version}")


@app.command()
def ping(config_file_path: Optional[str] = typer.Option(None, help="path to config file")):
    """
    Ping the current database connection
    """
    db_interactor = DatabaseInteractor(config_file_path)
    try:
        conn = db_interactor.conn
    except Exception as e:
        typer.echo("Something is wrong with the database connection!")
        raise
    else:
        typer.echo("Database connection looks good!")
        typer.echo(f"Database: {conn.info.dbname}")
        typer.echo(f"Host: {conn.info.host}")
