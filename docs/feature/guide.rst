Step-by-step Guide
=======================


- This page explains how the CLI can be used




Check version
---------------
.. literalinclude:: ../_static/code_snippet/guide/1-check_version.log


Initialise configuration File
-------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/2-init_config_file.log


Create Test Database
-------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/3-create_test_db.log


Create Test Database
-------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/4-update_config_yaml_file.log


Populate sample_database_revision_files_folder
----------------------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/5-populate_database_revision_files_folder.log

Ping the database
----------------------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/6-ping-db.log


Initialise the database
----------------------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/7-init-db.log

Check Current Database Version
----------------------------------------------------
.. literalinclude:: ../_static/code_snippet/guide/8-check-curr-db-version.log

Do Dry-run for db upgrade
----------------------------------------------------

- Check the logs to console and ensure the SQL file to be applied is really the correct one.

.. literalinclude:: ../_static/code_snippet/guide/9-db-upgrade-dry-run.log

Run DB Upgrade
----------------------------------------------------

- Upgrade the DB and check the db version afterwards

.. literalinclude:: ../_static/code_snippet/guide/10-db-upgrade.log


Use --head
----------------------------------------------------

- Check the SQL file(s) to be applied with the --head flag

.. literalinclude:: ../_static/code_snippet/guide/11-db-upgrade-with-head.log


Use --head
----------------------------------------------------

- Check the result in the database

.. literalinclude:: ../_static/code_snippet/guide/12-check-db-tables.log


Downgrade the database with --base and --no-confirm
----------------------------------------------------

- Check the result in the database

.. literalinclude:: ../_static/code_snippet/guide/13-downgrade-db-with-base-and-no-confirm.log


Check Database tables again
----------------------------------------------------

- Check the result in the database

.. literalinclude:: ../_static/code_snippet/guide/14-check_db_tables.log

