"""
config subcommand
"""

import typer
from pathlib import Path
from typing import List
import logging
import shutil

from dvc.core.config import get_matched_files_in_folder_by_regex, ConfigDefault, \
    get_revision_number_from_database_revision_file, DatabaseRevisionFilesManager, ConfigReader
from dvc.core.struct import Operation

app = typer.Typer()


@app.command()
def generate(from_sql_folder: str = typer.Option(..., help="Folder path with SQL files from which to generate Database Revsion Files")):
    """
    Generate RV upgrade files from all the SQLs files in a given directory
    """
    # Step 1: Get path of Source SQL files
    from_sql_folder_path = Path(from_sql_folder)
    logging.info(f"Sourcing from SQL folder: {from_sql_folder_path}")

    # Step 2: Get path of Database Revision SQL files
    config_file_reader = ConfigReader(ConfigDefault.VAL__FILE_PATH)
    db_rv_files_man = DatabaseRevisionFilesManager(config_file_reader)
    to_sql_folder_path = db_rv_files_man.database_revision_files_folder
    logging.info(f"Dumping to from database revision folder: {to_sql_folder_path}")

    # Step 3: Get latest RV
    existing_rv_file_name_regex = rf".*\.{Operation.Upgrade.value}\.sql"
    existing_rv_files = db_rv_files_man.get_database_revision_files_by_regex(existing_rv_file_name_regex)

    if len(existing_rv_files) == 0:
        latest_database_revision_number = 0
    else:
        existing_rv_files.sort(key=lambda sql_path: get_revision_number_from_database_revision_file(sql_path), reverse=True)
        latest_database_revision_number = get_revision_number_from_database_revision_file(existing_rv_files[0])

    logging.info(f"Latest database revision is {latest_database_revision_number}")

    # Step 4: Generate new RV files
    source_sql_file_name_regex = rf".*\.sql"
    source_sql_files_paths: List[Path] = get_matched_files_in_folder_by_regex(
        folder_path=from_sql_folder_path,
        file_name_regex=source_sql_file_name_regex
    )

    if len(source_sql_files_paths) == 0:
        logging.warning(f"No files found in folder {from_sql_folder}!")
        typer.Abort()

    next_new_database_revision_number = latest_database_revision_number + 1

    for source_sql_file_path in source_sql_files_paths:
        source_sql_file_path: Path = source_sql_file_path
        target_sql_file_path = to_sql_folder_path.joinpath(f"RV{next_new_database_revision_number}__{source_sql_file_path.stem}.{Operation.Upgrade.value}.sql")

        logging.info(f"Copying {source_sql_file_path} to {target_sql_file_path}...")
        confirm = typer.confirm("Are you sure?")
        if confirm:
            shutil.copy(str(source_sql_file_path), str(target_sql_file_path))
            next_new_database_revision_number += 1
        else:
            continue

