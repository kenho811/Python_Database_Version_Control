"""
config subcommand
"""

import typer
from pathlib import Path
import logging

from dvc.core.config import write_default_config_file
from dvc.core.struct import Operation

app = typer.Typer()


@app.command()
def generate(from_sql_folder: str = typer.Option(..., help="Folder path with SQL files from which to generate Database Revsion Files")):
    """
    Generate RV upgrade files from a given directory
    """
    # Get path of Source SQL files
    from_sql_folder_path = Path(from_sql_folder)
    logging.info(f"Sourcing from SQL folder: {from_sql_folder_path}")

    # Get path of Database Revision SQL files
    user_config = read_config_file(Default.CONFIG_FILE_PATH)
    to_sql_folder_path = Path(user_config['database_revision_sql_files_folder'])
    logging.info(f"Dumping to from database revision folder: {to_sql_folder_path}")

    # Get latest RV
    file_name_regex = f"*\.{Operation.Upgrade.value}\.sql"
    prog = re.compile(file_name_regex)

