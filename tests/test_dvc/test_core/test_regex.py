import logging
from typing import List

import pytest
from pathlib import Path

from dvc.core.regex import get_matched_files_in_folder_by_regex


@pytest.mark.unit
class TestGetMatchedFilesInFolderByRegex:

    @pytest.mark.parametrize(
        "file_name_regex,expected_num_matched_files_paths",
        [(r'.*\.sql', 4),
         (r'.*\.upgrade\.sql', 2),
         (r'RV1__.*\.sql', 2)
         ])
    def test__get_matched_files_in_folder_by_regex__assert_number_sql_files(
            self,
            dummy_regex_files_folder_with_correct_files_names,
            file_name_regex,
            expected_num_matched_files_paths
    ):
        """
        GIVEN a dummy folder with dummy files
        WHEN get_matched_files_in_folder_by_regex is called with a certain regex
        THEN the returned paths should match the regex
        """
        ## Act
        txt_matched_files_paths: List[Path] = get_matched_files_in_folder_by_regex(
            folder_path=dummy_regex_files_folder_with_correct_files_names,
            file_name_regex=file_name_regex,
        )

        ## Assert
        assert len(txt_matched_files_paths) == expected_num_matched_files_paths
