"""
database subcommand
"""

import logging
from typing import List, Optional
from pathlib import Path
import typer

from dvc.core.struct import DatabaseRevisionFile, Operation, DatabaseVersion
from dvc.core.config import DatabaseRevisionFilesManager, ConfigDefault

from dvc.app.cli.commands.database.backend import DatabaseInteractor
from dvc.core.logger import SetRootLoggingLevel

app = typer.Typer()


@app.command()
@SetRootLoggingLevel
def init(
        config_file_path: str = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
) -> None:
    """
    Generate configuration template & Initialise database

    :param config_file_path: String pointing to the path where configuration file is located
    :return:
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
@SetRootLoggingLevel
def upgrade(
        config_file_path: str = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying'),
        confirm: bool = typer.Option(True, help='Prompt user to confirm operation or not.'),
        steps: int = typer.Option(1, help='Number of steps to upgrade.'),
        head: bool = typer.Option(False, help='Whether to upgrade all the way to the latest Database Revision file found '),
        dry_run: bool = typer.Option(False, help='if True, do not apply any SQL files to the database'),
) -> None:
    """
    Upgrade the Current Database Version by applying a corresponding Upgrade Revision Version

    :param config_file_path: String pointing to the path where configuration file is located
    :param mark_only: whether or not to mark the SQL file as being done as metadata, without actually executing the SQL file
    :param confirm: whether or not to prompt user for confirmation
    :param steps: Number of steps requested to downgrade the database version
    :param head:
    :param dry_run:
    :return:
    """
    # Valid inpudt
    steps = abs(steps)

    if steps == 0:
        logging.error("Steps cannot be 0!")
        raise typer.Abort("Steps cannot be 0!")

    if head:
        pointer = DatabaseRevisionFilesManager.Pointer.HEAD
    else:
        pointer = None

    # Step 2: Output current database version
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version

    typer.echo(f"Current Database Version is {latest_database_version.version}")
    typer.echo( f"Next Upgrade Revision Version will be {latest_database_version.next_upgrade_database_revision_file.revision_number}")

    # Step 3: Get target revision files
    target_database_revision_files = db_interactor.get_target_database_revision_files(
        steps=steps,
        pointer=pointer
    )

    typer.echo("Below files will be applied:")
    typer.echo(target_database_revision_files)

    if dry_run:
        logging.info("Dry run is complete")
        raise typer.Abort()

    # Step 4: Run

    for target_database_revision_file in target_database_revision_files:
        typer.echo(f"Going to apply file {target_database_revision_file} .....")

        if confirm:
            resp = typer.confirm("You sure you want to continue ?")
            if not resp:
                raise typer.Abort()

        db_interactor.execute_single_sql_file(mark_only=mark_only,
                                              database_revision_file=target_database_revision_file)


@app.command()
@SetRootLoggingLevel
def downgrade(
        config_file_path: str = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
        mark_only: bool = typer.Option(False, help='Only mark the SQL file to metadata table without applying'),
        confirm: bool = typer.Option(True, help='Prompt user to confirm operation or not.'),
        steps: int = typer.Option(1, help='Number of steps to downgrade'),
        base: bool = typer.Option(False, help='Whether to downgrade all the way to the earliest Database Revision file found '),
        dry_run: bool = typer.Option(False, help='if True, do not apply any SQL files to the database'),
) -> None:
    """
    Downgrade the Current Database Version by applying a corresponding Downgrade Revision Version

    :param config_file_path: String pointing to the path where configuration file is located
    :param mark_only: mark the SQL file as being done as metadata, without actually executing the SQL file
    :param confirm: whether or not to prompt user for confirmation
    :param steps: Number of steps requested to downgrade the database version
    :param base:
    :param dry_run:
    :return:
    """
    # Step 1: Get the number of steps
    steps = abs(steps) * (-1)
    if steps == 0:
        logging.error("Steps cannot be 0!")
        raise typer.Abort()

    if base:
        pointer = DatabaseRevisionFilesManager.Pointer.BASE
    else:
        pointer = None

    # Step 2: Output current database version
    db_interactor = DatabaseInteractor(config_file_path_str=config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version

    typer.echo(f"Current Database Version is {latest_database_version.version}")
    typer.echo(
        f"Next Downgrade Revision Version will be {latest_database_version.next_downgrade_database_revision_file.revision_number}")

    # Step 3: Get target database revision files
    target_database_revision_files = db_interactor.get_target_database_revision_files(
        steps=steps,
        pointer=pointer,
    )

    typer.echo("Below files will be applied:")
    typer.echo(target_database_revision_files)

    if dry_run:
        logging.info("Dry run is complete")
        raise typer.Abort()

    # Step 4: Run

    for target_database_revision_file in target_database_revision_files:
        typer.echo(f"Going to apply file {target_database_revision_file} .....")

        if confirm:
            resp = typer.confirm("You sure you want to continue ?")
            if not resp:
                raise typer.Abort()

        db_interactor.execute_single_sql_file(mark_only=mark_only,
                                              database_revision_file=target_database_revision_file)


@app.command()
@SetRootLoggingLevel
def current(
        config_file_path: str = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
) -> None:
    """
    Check the current Database Version

    :param config_file_path: String pointing to the path where configuration file is located
    :return:
    """
    db_interactor = DatabaseInteractor(config_file_path)
    latest_database_version: DatabaseVersion = db_interactor.latest_database_version
    typer.echo(f"Database Current Version: {latest_database_version.version}")


@app.command()
@SetRootLoggingLevel
def ping(
        config_file_path: str = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
) -> None:
    """
    Ping the current database connection

    :param config_file_path: String pointing to the path where configuration file is located
    :return:
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
