import pytest
from pathlib import Path
from contextlib import nullcontext as does_not_raise

from dvc.core.struct import DatabaseRevisionFile
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
