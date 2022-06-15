"""
database subcommand
"""

import logging
from typing import List, Optional
from pathlib import Path
import typer

from dvc.core.struct import DatabaseRevision, Operation, DatabaseVersion

from dvc.app.cli.commands.database.backend import DatabaseInteractor
from dvc.app.cli.commands.database.backend import get_target_database_revision_sql_files

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
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying')):
    """
    Upgrade the Current Database Version by applying a corresponding Upgrade Revision Version
    """
    # Step 1: Check latest database version
    operation_type = Operation.Upgrade
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.get_latest_database_version()

    typer.echo(f"Current Database Version is {latest_database_version.current_version}")
    typer.echo(f"Next Upgrade Revision Version will be {latest_database_version.next_upgrade_revision_version}")

    target_sql_files = db_interactor.get_target_revision_sql_files(operation_type=operation_type)
    db_interactor.execute_sql_files(mark_only=mark_only,
                                    operation_type=operation_type,
                                    sql_files_paths=target_sql_files)



@app.command()
def downgrade(
        config_file_path: Optional[str] = typer.Option(None, help="path to config file"),
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying')
):
    """
    Downgrade the Current Database Version by applying a corresponding Downgrade Revision Version
    :return:
    """
    # Step 1: Check latest database version
    operation_type = Operation.Downgrade
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.get_latest_database_version()

    typer.echo(f"Current Database Version is {latest_database_version.current_version}")
    typer.echo(f"Next Downgrade Revision Version will be {latest_database_version.next_downgrade_revision_version}")

    target_sql_files = db_interactor.get_target_revision_sql_files(operation_type=operation_type)
    db_interactor.execute_sql_files(mark_only=mark_only,
                                    operation_type=operation_type,
                                    sql_files_paths=target_sql_files)


@app.command()
def current(config_file_path: Optional[str] = typer.Option(None, help="path to config file")):
    """
    Check the current Database Version
    :return:
    """
    db_interactor = DatabaseInteractor(config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.get_latest_database_version()
    typer.echo(f"Database Current Version: {latest_database_version.current_version}")


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
