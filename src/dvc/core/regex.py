from pathlib import Path
from typing import Dict, List
import logging
import re


def get_matched_files_in_folder_by_regex(folder_path: Path,
                                         file_name_regex: str,
                                         ) -> List[Path]:
    """
    Loop recursively for all files in a given folder.
    Return those files whose name satisfy the regex.
    :return:
    """
    matched_files_paths: List[Path] = []
    logging.info(f"Looking for the files with regex: {file_name_regex} in folder {folder_path}")
    prog = re.compile(file_name_regex)

    for file_or_dir in folder_path.glob('**/*'):
        file_or_dir: Path = file_or_dir
        if file_or_dir.is_file() and prog.match(file_or_dir.name):
            matched_files_paths.append(file_or_dir)

    return matched_files_paths
