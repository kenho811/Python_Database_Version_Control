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

