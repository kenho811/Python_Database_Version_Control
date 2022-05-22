from typing import Optional, List
from pathlib import Path
import re
import logging

from dvc.core.struct import Operation
from dvc.core.config import Default, DatabaseRevisionFilesManager, ConfigFileReader


def get_target_database_revision_sql_files(
        operation_type: Operation,
        target_revision_version: str,
) -> List[Path]:
    file_name_regex = f"{target_revision_version}__.*\.{operation_type.value}\.sql"

    # Get path of Database Revision SQL files
    config_file_reader = ConfigFileReader(Default.CONFIG_FILE_PATH)
    db_rv_files_man = DatabaseRevisionFilesManager(config_file_reader)
    matched_paths = db_rv_files_man.get_database_revision_files_by_regex(file_name_regex=file_name_regex)
    return matched_paths
