from typing import Optional, List
from pathlib import Path
import re
import logging

from dvc.core.struct import Operation
from dvc.core.config import get_matched_files_in_folder_by_regex, read_config_file, Default


def get_target_database_revision_sql_files(
        operation_type: Operation,
        target_revision_version: str,
) -> List[Path]:
    file_name_regex = f"{target_revision_version}.*\.{operation_type.value}\.sql"

    # Get path of Database Revision SQL files
    user_config = read_config_file(Default.CONFIG_FILE_PATH)
    database_revision_sql_files_folder_path = Path(user_config['database_revision_sql_files_folder'])
    matched_paths: List[Path] = get_matched_files_in_folder_by_regex(
        folder_path=database_revision_sql_files_folder_path,
        file_name_regex=file_name_regex
    )

    return matched_paths
