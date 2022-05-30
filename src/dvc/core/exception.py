from enum import Enum

from dvc.core.database import SupportedDatabaseFlavour



class RequestedDatabaseFlavourNotSupportedException(Exception):
    def __init__(self,
                 requested_database_flavour,
                 ):
        self.requested_database_flavour = requested_database_flavour

    def __str__(self):
        return f"""
        Your requested database flavour: {self.requested_database_flavour}
        Supported Database Flavours are:
        {[e.name for e in SupportedDatabaseFlavour]}
        """


class InvalidDatabaseRevisionFilesException(Exception):

    class Status(Enum):
        """
        List of all reasons
        """
        NON_CONFORMANT_REVISION_FILE_NAME_EXISTS = 101    # all files all follow 'RV{num}__{description}.{upgrade/downgrade}.sql' format
        MULTIPLE_REVISION_FILE_WITH_SAME_RV_NUMBER_EXISTS = 102  # No two revision files shoudl share i. same RV and ii. same upgrade/downgrade.

    def __init__(self,
                 status: Status
                 ,
                 ):
        self.status = status

    def __str__(self):
        return self.status.name
