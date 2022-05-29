from pathlib import Path
import logging


def validate_file_exist(
        file_path: Path) -> None:
    """
    Throw FileNotFileError if a given file does not exist
    """
    if not file_path.is_file():
        err_msg = f"File Path {file_path} does not exist!"
        logging.error(err_msg)
        raise FileNotFoundError(err_msg)
