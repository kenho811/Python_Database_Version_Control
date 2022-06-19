Database Metadata
=========================

Just like git which stores all the metadata in a dot git folder (.git), the tool also stores metadata in the database where SQL Revision Files are applied.


- Schema dvc will be created

  - Table dvc.database_revision_history will be created.
        - History of revision SQL files applied.

  - Table dvc.database_version_history will be created.
        - History of database versions which result from revision SQL files applied.
