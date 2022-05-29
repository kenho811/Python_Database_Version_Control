import logging
from typing import List

import pytest
from pathlib import Path

from dvc.core.regex import get_matched_files_in_folder_by_regex


@pytest.fixture()
def dummy_regex_files_folder(tmp_path):
    regex_files_folder: Path = tmp_path.joinpath('regex_files_folder')
    regex_files_folder.mkdir(parents=True, exist_ok=True)
    return regex_files_folder


@pytest.fixture()
def generate_files(dummy_regex_files_folder):
    # Set up
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
    yield

    # Tear down
    for dummy_file_name in DUMMY_FILE_NAMES:
        logging.info(f"deleting file {dummy_regex_files_folder.joinpath(dummy_file_name)}")
        dummy_regex_files_folder.joinpath(dummy_file_name).unlink()


@pytest.mark.usefixtures('generate_files')
class TestGetMatchedFilesInFolderByRegex:
    """
    GIVEN a dummy folder with dummy files
    WHEN get_matched_files_in_folder_by_regex is called with a certain regex
    THEN the returned paths should match the regex
    """
    def test__get_matched_files_in_folder_by_regex__assert_number_sql_files(
            self,
            dummy_regex_files_folder):
        """
        regex is file ending
        """
        ## Arrange
        file_name_regex = r'.*\.sql'
        ## Act
        txt_matched_files_paths: List[Path] = get_matched_files_in_folder_by_regex(
            folder_path=dummy_regex_files_folder,
            file_name_regex=file_name_regex,
        )

        ## Assert
        assert len(txt_matched_files_paths) == 4

    def test__get_matched_files_in_folder_by_regex__assert_number_upgrade_sql_files(
            self,
            dummy_regex_files_folder):
        """
        regex is file ending
        """
        ## Arrange
        file_name_regex = r'.*\.upgrade\.sql'
        ## Act
        txt_matched_files_paths: List[Path] = get_matched_files_in_folder_by_regex(
            folder_path=dummy_regex_files_folder,
            file_name_regex=file_name_regex,
        )

        ## Assert
        assert len(txt_matched_files_paths) == 2


    def test__get_matched_files_in_folder_by_regex__assert_number_rv1_files(
            self,
            dummy_regex_files_folder):
        """
        regex is file ending
        """
        ## Arrange
        file_name_regex = r'RV1__.*\.sql'
        ## Act
        txt_matched_files_paths: List[Path] = get_matched_files_in_folder_by_regex(
            folder_path=dummy_regex_files_folder,
            file_name_regex=file_name_regex,
        )

        ## Assert
        assert len(txt_matched_files_paths) == 2

