import pytest
from dvc.core.struct import DatabaseVersion, DatabaseRevision, Operation

from tests.assets import TEST_REVISION_SQL_FILES_FOLDER_PATH

# RV!
@pytest.fixture()
def rv1_upgrade_database_revision():
    path = TEST_REVISION_SQL_FILES_FOLDER_PATH.joinpath('RV1__create_scm_fundamentals_and_tbls.upgrade.sql')
    operation = Operation.Upgrade
    db_rev = DatabaseRevision(executed_sql_file_path_applied=path,
                              operation=operation)
    return db_rev

@pytest.fixture()
def rv1_downgrade_database_revision():
    path = TEST_REVISION_SQL_FILES_FOLDER_PATH.joinpath('RV1__create_scm_fundamentals_and_tbls.downgrade.sql')
    operation = Operation.Downgrade
    db_rev = DatabaseRevision(executed_sql_file_path_applied=path,
                              operation=operation)
    return db_rev


# RV2
@pytest.fixture()
def rv2_upgrade_database_revision():
    path = TEST_REVISION_SQL_FILES_FOLDER_PATH.joinpath('RV2__create_scm_datetime_and_tbls.upgrade.sql')
    operation = Operation.Upgrade
    db_rev = DatabaseRevision(executed_sql_file_path_applied=path,
                              operation=operation)
    return db_rev



@pytest.fixture()
def rv2_downgrade_database_revision():
    path = TEST_REVISION_SQL_FILES_FOLDER_PATH.joinpath('RV2__create_scm_datetime_and_tbls.downgrade.sql')
    operation = Operation.Downgrade
    db_rev = DatabaseRevision(executed_sql_file_path_applied=path,
                              operation=operation)
    return db_rev
