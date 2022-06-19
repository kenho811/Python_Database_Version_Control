import pytest
from pathlib import Path
from contextlib import nullcontext as does_not_raise
from typing import List

from dvc.core.struct import DatabaseRevisionFile, DatabaseVersion, Operation
from dvc.core.exception import InvalidDatabaseRevisionFilesException


class TestDatabaseRevisionFile:

    @pytest.mark.parametrize("sql_file_name, expectation",
                             [
                                 # Normal Files
                                 ("RV1__hello_world.upgrade.sql", does_not_raise()),
                                 ("RV2__byebye.downgrade.sql", does_not_raise()),

                                 # No revision number
                                 ("RV__byebye.downgrade.sql", pytest.raises(InvalidDatabaseRevisionFilesException)),

                                 # No `RV` prefix
                                 ("2_.downgrade.sql", pytest.raises(InvalidDatabaseRevisionFilesException)),

                                 # Single underscore
                                 ("RV1_dsds.downgrade.sql", pytest.raises(InvalidDatabaseRevisionFilesException)),

                                 # Neither upgrade nor downgrade
                                 ("RV1__dsds.zerograde.sql", pytest.raises(InvalidDatabaseRevisionFilesException)),

                                 # Not SQL file
                                 ("RV2__byebye.downgrade.txt", pytest.raises(InvalidDatabaseRevisionFilesException)),
                             ]
                             )
    def test_valid_database_revision_files(self,
                                           sql_file_name: str,
                                           expectation,
                                           ):
        with expectation:
            assert DatabaseRevisionFile(Path(sql_file_name)) is not None


class TestDatabaseVersion:

    @pytest.mark.parametrize("target_database_version,current_database_version,expected_dummy_database_revision_files",
                             [
                                 # When target version > Current, return upgrade files
                                 (DatabaseVersion(current_version="V3"), DatabaseVersion(current_version="V1"), [
                                         DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV2",
                                                                                      operation_type=Operation.Upgrade),
                                         DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV3",
                                                                                      operation_type=Operation.Upgrade),
                                 ]),

                                 # When target version < Current, return downgrade files
                                 (DatabaseVersion(current_version="V1"), DatabaseVersion(current_version="V3"), [
                                     DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV3",
                                                                                  operation_type=Operation.Downgrade),
                                     DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV2",
                                                                                  operation_type=Operation.Downgrade),
                                 ]),

                                 # When target version = Current, return nothing
                                 (DatabaseVersion(current_version="V1"), DatabaseVersion(current_version="V1"), [
                                 ]),
                             ]
                             )
    def test_valid_dummy_database_revision_files(
            self,
            target_database_version: DatabaseVersion,
            current_database_version: DatabaseVersion,
            expected_dummy_database_revision_files: List[DatabaseRevisionFile],
    ):
        actual_dummy_database_revision_files = target_database_version - current_database_version
        actual_dummy_database_revision_files.sort(reverse=False)
        expected_dummy_database_revision_files.sort(reverse=False)

        assert actual_dummy_database_revision_files == expected_dummy_database_revision_files
