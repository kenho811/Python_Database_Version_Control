"""
config subcommand
"""
import logging

import typer
from typing import Dict
from pathlib import Path

from dvc.core.config import write_default_config_file, generate_database_revision_sql_folder, read_config_file, Default

app = typer.Typer()


@app.command()
def init():
    """
    Generate configuration template
    """
    # Step 1: Generate config file
    write_default_config_file()

    # Step 2: Generate Datababase Revision SQL folder
    generate_database_revision_sql_folder(Default.CONFIG_FILE_PATH)
