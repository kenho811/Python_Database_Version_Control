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

    @pytest.mark.parametrize("file_1,file_2,predicate,expected",
                             [
                                 (DatabaseRevisionFile.get_dummy_revision_file(revision="RV2",
                                                                               operation_type=Operation.Upgrade),
                                  DatabaseRevisionFile.get_dummy_revision_file(revision="RV1",
                                                                               operation_type=Operation.Upgrade),
                                  'file_1 > file_2',
                                  False),
                                 (DatabaseRevisionFile.get_dummy_revision_file(revision="RV2",
                                                                               operation_type=Operation.Upgrade),
                                  DatabaseRevisionFile.get_dummy_revision_file(revision="RV1",
                                                                               operation_type=Operation.Downgrade),
                                  'file_1 > file_2',
                                  None),
                                 (
                                         DatabaseRevisionFile.get_dummy_revision_file(revision="RV2",
                                                                                      operation_type=Operation.Downgrade),
                                         DatabaseRevisionFile.get_dummy_revision_file(revision="RV1",
                                                                                      operation_type=Operation.Downgrade),
                                         'file_1 > file_2',
                                         False
                                 )
                             ])
    def test_database_revision_files_comparison(self,
                                                file_1,
                                                file_2,
                                                predicate,
                                                expected,
                                                ):
        assert (lambda file_1, file_2: eval(predicate) == expected)


class TestDatabaseVersion:

    @pytest.mark.parametrize("target_database_version,current_database_version,expected_dummy_database_revision_files",
                             [
                                 # When target version > Current, return upgrade files. Order from current to target
                                 (DatabaseVersion(version="V3"),
                                  DatabaseVersion(version="V1"),
                                  [DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV2",
                                                                                operation_type=Operation.Upgrade),
                                   DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV3",
                                                                                operation_type=Operation.Upgrade),
                                   ]),

                                 # When target version < Current, return downgrade files. Order from current to target
                                 (DatabaseVersion(version="V11"),
                                  DatabaseVersion(version="V13"),
                                  [DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV13",
                                                                                operation_type=Operation.Downgrade),
                                   DatabaseRevisionFile.get_dummy_revision_file(revision=f"RV12",
                                                                                operation_type=Operation.Downgrade),
                                   ]),

                                 # When target version = Current, return nothing
                                 (DatabaseVersion(version="V1"), DatabaseVersion(version="V1"), [
                                 ]),
                             ], scope='function'
                             )
    def test_valid_dummy_database_revision_files_with_order(
            self,
            target_database_version: DatabaseVersion,
            current_database_version: DatabaseVersion,
            expected_dummy_database_revision_files: List[DatabaseRevisionFile],
    ):
        actual_dummy_database_revision_files = target_database_version - current_database_version

        assert actual_dummy_database_revision_files == expected_dummy_database_revision_files
