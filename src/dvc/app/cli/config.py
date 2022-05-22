"""
config subcommand
"""
import logging

import typer
from typing import Dict
from pathlib import Path

from dvc.core.config import Default, DatabaseRevisionFilesManager, ConfigFileWriter

app = typer.Typer()


@app.command()
def init():
    """
    Generate configuration template
    """
    # Step 1: Generate config file
    ConfigFileWriter(config_file_path=Default.CONFIG_FILE_PATH).write_to_yaml()

    # Step 2: Generate Datababase Revision SQL folder
    db_rv_files_man = DatabaseRevisionFilesManager(config_file_path=Default.CONFIG_FILE_PATH)
    db_rv_files_man.create_database_revision_files_folder()
