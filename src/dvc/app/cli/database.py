"""
database subcommand
"""

import logging
import traceback
from typing import List
from pathlib import Path
import typer

from dvc.core.struct import DatabaseRevision, Operation, DatabaseVersion
from dvc.core.database.postgres import SQLFileExecutor
from dvc.core.config import get_postgres_connection

from dvc.app.backend import get_target_database_revision_sql_files

app = typer.Typer()


@app.command()
def init():
    """
    Generate configuration template & Initialise database
    """
    # Step 2: Set up metadata schema and tables
    conn = get_postgres_connection()
    sql_file_executor = SQLFileExecutor(conn=conn)
    sql_file_executor.set_up_database_revision_control_tables()


@app.command()
def upgrade(mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying')):
    """
    Upgrade the Current Database Version by applying a corresponding Upgrade Revision Version
    """
    # Step 1: Check latest database version
    operation_type = Operation.Upgrade
    conn = get_postgres_connection()
    sql_file_executor = SQLFileExecutor(conn=conn)
    latest_database_version: DatabaseVersion = sql_file_executor.get_latest_database_version()

    typer.echo(f"Current Database Version is {latest_database_version.current_version}")
    typer.echo(f"Next Upgrade Revision Version will be {latest_database_version.next_upgrade_revision_version}")

    # Step 2: Loop through existing revision SQL files
    target_upgrade_revision_files: List[Path] = get_target_database_revision_sql_files(
        operation_type=operation_type,
        target_revision_version=latest_database_version.next_upgrade_revision_version
    )

    if len(target_upgrade_revision_files) > 1:
        typer.echo("More than 1 target upgrade revision files found! As follows:")
        typer.echo(target_upgrade_revision_files)
        raise typer.Abort()
    elif len(target_upgrade_revision_files) == 0:
        typer.echo("No target upgrade revision files are found!")
        raise typer.Abort()

    # Step 3: Confirmation
    sql_file_path = target_upgrade_revision_files[0]
    apply = typer.confirm(f"Are you sure you want to apply the revision file at {sql_file_path}?")

    if apply and not mark_only:
        logging.info(f"Now applying {sql_file_path} and marking to metadata table")
        database_revision = DatabaseRevision(
            executed_sql_file_path_applied=sql_file_path,
            operation=operation_type
        )
        sql_file_executor = SQLFileExecutor(conn=conn)
        sql_file_executor.execute_database_revision(database_revision=database_revision)
    elif apply and mark_only:
        logging.info(f"Now only marking {sql_file_path} to metadata table")
        database_revision = DatabaseRevision(
            executed_sql_file_path_applied=sql_file_path,
            operation=operation_type
        )
        sql_file_executor = SQLFileExecutor(conn=conn)
        sql_file_executor._write_database_revision_metadata(database_revision=database_revision)
    else:
        logging.info(f"Do nothing...")
        typer.Abort()


@app.command()
def downgrade(mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying')):
    """
    Downgrade the Current Database Version by applying a corresponding Downgrade Revision Version
    :return:
    """
    # Step 1: Check latest database version
    operation_type = Operation.Downgrade
    conn = get_postgres_connection()
    sql_file_executor = SQLFileExecutor(conn=conn)
    latest_database_version: DatabaseVersion = sql_file_executor.get_latest_database_version()

    typer.echo(f"Current Database Version is {latest_database_version.current_version}")
    typer.echo(f"Next Downgrade Revision Version will be {latest_database_version.next_downgrade_revision_version}")

    # Step 2: Loop through existing revision SQL files
    target_downgrade_revision_files: List[Path] = get_target_database_revision_sql_files(
        operation_type=operation_type,
        target_revision_version=latest_database_version.next_downgrade_revision_version
    )

    if len(target_downgrade_revision_files) > 1:
        typer.echo("More than 1 target downgrade revision files found! As follows:")
        typer.echo(target_downgrade_revision_files)
        raise typer.Abort()
    elif len(target_downgrade_revision_files) == 0:
        typer.echo("No target downgrade revision files are found!")
        raise typer.Abort()

    sql_file_path = target_downgrade_revision_files[0]
    apply = typer.confirm(f"Are you sure you want to apply the revision file at {sql_file_path}?")

    if apply and not mark_only:
        logging.info(f"Now applying {sql_file_path} and marking to metadata table")
        database_revision = DatabaseRevision(
            executed_sql_file_path_applied=sql_file_path,
            operation=operation_type
        )
        sql_file_executor = SQLFileExecutor(conn=conn)
        sql_file_executor.execute_database_revision(database_revision=database_revision)
    elif apply and mark_only:
        logging.info(f"Now only marking {sql_file_path} to metadata table")
        database_revision = DatabaseRevision(
            executed_sql_file_path_applied=sql_file_path,
            operation=operation_type
        )
        sql_file_executor = SQLFileExecutor(conn=conn)
        sql_file_executor._write_database_revision_metadata(database_revision=database_revision)
    else:
        logging.info(f"Do nothing...")
        typer.Abort()


@app.command()
def current():
    """
    Check the current Database Version
    :return:
    """
    conn = get_postgres_connection()
    sql_file_executor = SQLFileExecutor(conn=conn)
    latest_database_version: DatabaseVersion = sql_file_executor.get_latest_database_version()
    typer.echo(latest_database_version)


@app.command()
def ping():
    """
    Ping the current database connection
    """
    try:
        get_postgres_connection()
    except Exception as e:
        logging.error(traceback.format_exc())
        typer.echo("Something is wrong with the database connection!")
    else:
        typer.echo("Database connection looks good!")
