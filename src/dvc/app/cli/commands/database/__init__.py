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
        steps: int = typer.Option(1, help='Number of steps to upgrade.'),
):
    """
    Upgrade the Current Database Version by applying a corresponding Upgrade Revision Version
    """
    # Step 1: Check latest database version
    steps = abs(steps)

    if steps == 0:
        logging.error("Steps cannot be 0!")
        raise typer.Abort("Steps cannot be 0!")

    # Step 2: Output current database version
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version

    typer.echo(f"Current Database Version is {latest_database_version.version}")
    typer.echo(f"Next Upgrade Revision Version will be {latest_database_version.next_upgrade_database_revision_file.revision_number}")

    target_database_revision_files = db_interactor.get_target_database_revision_files(steps=steps)

    # Step 3: Run
    for target_database_revision_file in target_database_revision_files:
        logging.info(f"Going to apply file {target_database_revision_file} .....")

        if confirm:
            resp = typer.confirm("You sure you want to continue ?")
            if not resp:
                raise typer.Abort()

        db_interactor.execute_single_sql_file(mark_only=mark_only,
                                              database_revision_file=target_database_revision_file)




@app.command()
def downgrade(
        config_file_path: Optional[str] = typer.Option(None, help="path to config file"),
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying'),
        confirm: bool = typer.Option(True, help='Prompt user to confirm operation or not.'),
        steps: int = typer.Option(1, help='Number of steps to downgrade'),
):
    """
    Downgrade the Current Database Version by applying a corresponding Downgrade Revision Version
    :return:
    """
    # Step 1: Get the number of steps
    steps = abs(steps) * (-1)
    if steps == 0:
        logging.error("Steps cannot be 0!")
        raise typer.Abort()


    # Step 2: Output current database version
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version

    typer.echo(f"Current Database Version is {latest_database_version.version}")
    typer.echo(f"Next Downgrade Revision Version will be {latest_database_version.next_downgrade_database_revision_file.revision_number}")

    # Step 3: Run
    target_database_revision_files = db_interactor.get_target_database_revision_files(steps=steps)

    for target_database_revision_file in target_database_revision_files:
        logging.info(f"Going to apply file {target_database_revision_file} .....")

        if confirm:
            resp = typer.confirm("You sure you want to continue ?")
            if not resp:
                raise typer.Abort()

        db_interactor.execute_single_sql_file(mark_only=mark_only,
                                              database_revision_file=target_database_revision_file)


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
