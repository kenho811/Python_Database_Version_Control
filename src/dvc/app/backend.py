from typing import Optional, List
from pathlib import Path
import re
import logging

from dvc.core.struct import Operation
from dvc.core.config import get_database_revision_sql_files


def get_target_database_revision_sql_files(
        operation_type: Operation,
        target_revision_version: str,
) -> List[Path]:
    matched_paths: List[Path] = []
    file_name_regex = f"{target_revision_version}.*\.{operation_type.value}\.sql"

    logging.info(f"Looking for the sql files with regex: {file_name_regex}")

    prog = re.compile(file_name_regex)

    for sql_file_path in get_database_revision_sql_files():
        sql_file_path: Path = sql_file_path
        sql_file_name: str = sql_file_path.name
        if prog.match(sql_file_name):
            matched_paths.append(sql_file_path)

    return matched_paths
