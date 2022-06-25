import logging
from unittest import mock
import pytest
from contextlib import nullcontext as does_not_raise

from dvc.core.database import SupportedDatabaseFlavour
from dvc.core.config import DatabaseConnectionFactory, ConfigDefault, ConfigFileWriter, ConfigReader, \
    DatabaseRevisionFilesManager
from dvc.core.exception import RequestedDatabaseFlavourNotSupportedException, InvalidDatabaseRevisionFilesException, \
    EnvironmentVariableNotSetException, InvalidDatabaseVersionException
from dvc.core.struct import DatabaseVersion, DatabaseRevisionFile, Operation


@pytest.mark.unit
class TestConfigFileWriter:

    def test__write_dummy_user_configuration(
            self,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_absent_config_file_path,
    ):
        """
        GIVEN a non-existing config file path
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Action
        ConfigFileWriter(dummy_absent_config_file_path).write_to_yaml()

        # Assert
        assert dummy_absent_config_file_path.is_file()


@pytest.mark.unit
class TestConfigReader:

    def test__when_both_config_file_and_env_var_and_absent__raise_environment_variables_not_set_exception(
            self,
            dummy_absent_config_file_path,
    ):
        """
        GIVEN a dummy config file with dummy user configuration,
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Action
        with pytest.raises(EnvironmentVariableNotSetException) as exc_info:
            user_config = ConfigReader(dummy_absent_config_file_path).user_config

    def test__when_config_file_is_absent_but_env_var_present__return_expected_user_config_from_env_var(
            self,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_absent_config_file_path_with_env_var,
            monkeypatch,
    ):
        """
        GIVEN a dummy config file with dummy user configuration,
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Action
        user_config = ConfigReader(dummy_absent_config_file_path_with_env_var).user_config

        # Assert
        assert user_config == dummy_user_configuration_with_supported_db_flavour

    def test__when_config_file_is_persent__return_expected_user_config_from_config_file(
            self,
            dummy_user_configuration_with_supported_db_flavour,
            dummy_existing_config_file_path,
    ):
        """
        GIVEN a dummy config file with dummy user configuration,
        WHEN ConfigFileReader.user_config is called
        THEN check dummy user configuration is returned
        """
        # Action
        user_config = ConfigReader(dummy_existing_config_file_path).user_config

        # Assert
        assert user_config == dummy_user_configuration_with_supported_db_flavour


@pytest.mark.unit
class TestDatabaseRevisionFilesManager:

    @pytest.mark.parametrize(
        'current_database_version,candidate_database_revision_files,pointer,expected_database_revision_files,expected_exception',
        [
            #
            (DatabaseVersion(version='V0', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3', operation_type=Operation.Upgrade),
             ],
             DatabaseRevisionFilesManager.Pointer.HEAD,
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3', operation_type=Operation.Upgrade),
             ],
             does_not_raise()
             ),

            #
            (DatabaseVersion(version='V3', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
             ],
             DatabaseRevisionFilesManager.Pointer.BASE,
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1',
                                                              operation_type=Operation.Downgrade),
             ],
             does_not_raise()
             ),

            #
            (DatabaseVersion(version='V3', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
             ],
             DatabaseRevisionFilesManager.Pointer.BASE,
             [
                 # Pass. Expected to raise exception
             ],
             pytest.raises(InvalidDatabaseRevisionFilesException)
             ),

            #
            (DatabaseVersion(version='V0', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2',
                                                              operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Upgrade),
             ],
             DatabaseRevisionFilesManager.Pointer.HEAD,
             [
                 # Pass. Expected to raise exception
             ],
             pytest.raises(InvalidDatabaseRevisionFilesException)
             ),

        ]
        )
    def test__get_target_database_revision_files_by_pointer(
            self,
            dummy_config_file_reader_with_supported_db_flavour,
            current_database_version,
            candidate_database_revision_files,
            pointer,
            expected_database_revision_files,
            expected_exception
    ):
        # Act
        sut = DatabaseRevisionFilesManager(config_file_reader=dummy_config_file_reader_with_supported_db_flavour)
        with expected_exception:
            # May raise exception
            actual_database_revision_files = sut.get_target_database_revision_files_by_pointer(
                current_database_version=current_database_version,
                candidate_database_revision_files=candidate_database_revision_files,
                pointer=pointer)
            # If not raise exception, assert the below
            assert actual_database_revision_files == expected_database_revision_files

    @pytest.mark.parametrize(
        'current_database_version,candidate_database_revision_files,steps,expected_database_revision_files,expected_exception',
        [
            #
            (DatabaseVersion(version='V0', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3', operation_type=Operation.Upgrade),
             ],
             2,
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1', operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2', operation_type=Operation.Upgrade),
             ],
             does_not_raise()
             ),

            #
            (DatabaseVersion(version='V3', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
             ],
             -2,
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2',
                                                              operation_type=Operation.Downgrade),
             ],
             does_not_raise()
             ),

            #
            (DatabaseVersion(version='V3', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV1',
                                                              operation_type=Operation.Downgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
             ],
             -1,
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Downgrade),
             ],
             does_not_raise()
             ),

            #
            (DatabaseVersion(version='V0', created_at=None),
             [
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV2',
                                                              operation_type=Operation.Upgrade),
                 DatabaseRevisionFile.get_dummy_revision_file(revision='RV3',
                                                              operation_type=Operation.Upgrade),
             ],
             3,
             [
                 # Pass. Expected to raise exception
             ],
             pytest.raises(InvalidDatabaseRevisionFilesException)
             ),

        ]
    )
    def test__get_target_database_revision_files_by_pointer(
            self,
            dummy_config_file_reader_with_supported_db_flavour,
            current_database_version,
            candidate_database_revision_files,
            steps,
            expected_database_revision_files,
            expected_exception
    ):
        # Act
        sut = DatabaseRevisionFilesManager(config_file_reader=dummy_config_file_reader_with_supported_db_flavour)
        with expected_exception:
            # May raise exception
            actual_database_revision_files = sut.get_target_database_revision_files_by_steps(
                current_database_version=current_database_version,
                candidate_database_revision_files=candidate_database_revision_files,
                steps=steps,
            )
            # If not raise exception, assert the below
            assert actual_database_revision_files == expected_database_revision_files


@pytest.mark.unit
class TestDatabaseConnectionFactory:

    def test__raise_requested_database_not_supported_exception(
            self,
            dummy_config_file_reader_with_unsupported_db_flavour,
    ):
        """
        GIVEN a fake database flavour
        WHEN DatabaseConnectionFactory.validate_requested_database_flavour is called
        THEN assert RequestedDatabaseFlavourNotSupportedException is raised
        """
        # Assert
        with pytest.raises(RequestedDatabaseFlavourNotSupportedException) as exc_info:
            # Act
            DatabaseConnectionFactory(
                dummy_config_file_reader_with_unsupported_db_flavour).validate_requested_database_flavour()

    def test__pass_user_credentials_to_connect_as_kwargs(
            self,
            dummy_config_file_reader_with_supported_db_flavour,
            dummy_pgconn,
    ):
        """
        (Currently test postgres specifically)
        GIVEN patched psycopg2.connect
        WHEN DatabaseConnectionFactory.conn is called
        THEN check psycopg2.connect is called once and with expected args
        """
        # Act
        DatabaseConnectionFactory(config_reader=dummy_config_file_reader_with_supported_db_flavour).conn

        # Assert
        expects_args = {
            "dbname": 'superman_db',
            "user": 'peter_parker',
            "password": '1234',
            "port": 5432,
            "host": 'localhost',
        }
        dummy_pgconn.assert_called_once()
        dummy_pgconn.assert_called_with(
            **expects_args
        )
