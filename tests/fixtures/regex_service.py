import logging
from typing import List

import pytest
from pathlib import Path


@pytest.fixture()
def correct_files_names():
    CORRECT_DATABASE_REVISION_FILES = [
        'RV1__create_scm_fundamentals_and_tbls.downgrade.sql',
        'RV1__create_scm_fundamentals_and_tbls.upgrade.sql',
        'RV2__create_scm_datetime_and_tbls.downgrade.sql',
        'RV2__create_scm_datetime_and_tbls.upgrade.sql',
    ]
    return CORRECT_DATABASE_REVISION_FILES

@pytest.fixture()
def correct_but_duplicate_files_names():
    CORRECT_BUT_DUPLICATE_DATABASE_REVISION_FILES = [
        'RV1__create_scm_fundamentals_and_tbls.upgrade.sql',
        'RV1__create_scm_fundamentals_and_tbls.upgrade.sql',
        'RV2__create_scm_datetime_and_tbls.downgrade.sql',
        'RV2__create_scm_datetime_and_tbls.upgrade.sql',
    ]
    return CORRECT_BUT_DUPLICATE_DATABASE_REVISION_FILES


@pytest.fixture()
def incorrect_files_names():
    INCORRECT_DATABASE_REVISION_FILES = [
        'V1__create_scm_fundamentals_and_tbls.downgrade.sql',
        'RV1__create_scm_fundamentals_and_tbls.whatisthis.sql',
        'RV2__create_scm_datetime_and_tbls.downgrade.weirdFileEnding',
        'RV2__create_scm_datetime_and_tbls.upgrade.sql',
    ]
    return INCORRECT_DATABASE_REVISION_FILES


@pytest.fixture()
def dummy_regex_files_folder_with_correct_files_names(
        tmp_path,
        correct_files_names,
):
    """
    Set up the dummy regex files
    Yield the dummy regex files folder path
    Delete the dummy regex files afterwards
    """
    # Set up
    dummy_regex_files_folder: Path = tmp_path.joinpath('dummy_regex_files_folder_with_correct_files_names')
    dummy_regex_files_folder.mkdir(parents=True, exist_ok=True)

    for dummy_file_name in correct_files_names:
        with open(dummy_regex_files_folder.joinpath(dummy_file_name), 'w') as dummy_file:
            logging.info(f"creating file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
            dummy_file.write('123')

    # Return the path containing the dummy files
    yield dummy_regex_files_folder

    # Tear down
    for dummy_file_name in correct_files_names:
        logging.info(f"deleting file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
        dummy_regex_files_folder.joinpath(dummy_file_name).unlink()


@pytest.fixture()
def dummy_regex_files_folder_with_incorrect_files_names(
        tmp_path,
        incorrect_files_names,
):
    """
    Set up the dummy regex files
    Yield the dummy regex files folder path
    Delete the dummy regex files afterwards
    """
    # Set up
    dummy_regex_files_folder: Path = tmp_path.joinpath('dummy_regex_files_folder_with_incorrect_files_names')
    dummy_regex_files_folder.mkdir(parents=True, exist_ok=True)

    for dummy_file_name in incorrect_files_names:
        with open(dummy_regex_files_folder.joinpath(dummy_file_name), 'w') as dummy_file:
            logging.info(f"creating file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
            dummy_file.write('123')

    # Return the path containing the dummy files
    yield dummy_regex_files_folder

    # Tear down
    for dummy_file_name in incorrect_files_names:
        logging.info(f"deleting file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
        dummy_regex_files_folder.joinpath(dummy_file_name).unlink()

@pytest.fixture()
def dummy_regex_files_folder_with_correct_but_duplicate_files_names(
        tmp_path,
        correct_but_duplicate_files_names
):
    """
    Set up the dummy regex files
    Yield the dummy regex files folder path
    Delete the dummy regex files afterwards
    """
    # Set up
    dummy_regex_files_folder: Path = tmp_path.joinpath('dummy_regex_files_folder_with_incorrect_files_names')
    dummy_regex_files_folder.mkdir(parents=True, exist_ok=True)

    for dummy_file_name in correct_but_duplicate_files_names:
        with open(dummy_regex_files_folder.joinpath(dummy_file_name), 'w') as dummy_file:
            logging.info(f"creating file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
            dummy_file.write('123')

    # Return the path containing the dummy files
    yield dummy_regex_files_folder

    # Tear down
    for dummy_file_name in correct_but_duplicate_files_names:
        logging.info(f"deleting file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
        dummy_regex_files_folder.joinpath(dummy_file_name).unlink()
