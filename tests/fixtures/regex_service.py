import logging
from typing import List

import pytest
from pathlib import Path



@pytest.fixture()
def dummy_regex_files_folder(
        tmp_path, ):
    """
    Set up the dummy regex files
    Yield the dummy regex files folder path
    Delete the dummy regex files afterwards
    """
    # Set up
    dummy_regex_files_folder: Path = tmp_path.joinpath('dummy_regex_files_folder')
    dummy_regex_files_folder.mkdir(parents=True, exist_ok=True)

    DUMMY_FILE_NAMES = [
        'RV1__create_scm_fundamentals_and_tbls.downgrade.sql',
        'RV1__create_scm_fundamentals_and_tbls.upgrade.sql',
        'RV2__create_scm_datetime_and_tbls.downgrade.sql',
        'RV2__create_scm_datetime_and_tbls.upgrade.sql',
    ]
    for dummy_file_name in DUMMY_FILE_NAMES:
        with open(dummy_regex_files_folder.joinpath(dummy_file_name), 'w') as dummy_file:
            logging.info(f"creating file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
            dummy_file.write('123')

    # Return the path containing the dummy files
    yield dummy_regex_files_folder

    # Tear down
    for dummy_file_name in DUMMY_FILE_NAMES:
        logging.info(f"deleting file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
        dummy_regex_files_folder.joinpath(dummy_file_name).unlink()
