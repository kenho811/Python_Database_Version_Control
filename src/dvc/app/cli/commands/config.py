"""
config subcommand
"""
import logging

import typer
from typing import Optional

from dvc.core.config import ConfigDefault, DatabaseRevisionFilesManager, ConfigFileWriter, ConfigReader

app = typer.Typer()


@app.command()
def init(
        config_file_path: Optional[str] = typer.Option(str(ConfigDefault.VAL__FILE_PATH), help="path to config file"),
) -> None:
    """
    Generate configuration template. Idempotent.

    :return:
    """
    # Step 1: Generate config file
    config_file_writer = ConfigFileWriter(config_file_path=config_file_path)
    config_file_writer.write_to_yaml()

    # Step 2: Generate Datababase Revision SQL folder
    config_file_reader = ConfigReader(config_file_path)
    db_rv_files_man = DatabaseRevisionFilesManager(config_file_reader)
    db_rv_files_man.create_database_revision_files_folder()
