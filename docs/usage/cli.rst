CLI
==============

This page explains how to use the tool packaged as commandline tool (CLI).

A typical workflow is as follows:

.. code-block:: rst

    # Generate configuration file
    dvc cfg init

    # Update the generated config.yaml

    # Test connection to the database with the updated config.ayml
    dvc db ping

    # Test connection to the database with the updated config.ayml
    dvc db ping

    # Create a folder to store all the SQL files to be applied to the database
    # Remember to use the same folder name as specified in the config.yaml file

    # Make sure the SQL files follow the naming conventions.

    # Run upgrade script
    dvc db upgrade

    # (Optional) To revert the migration, create a downgrade script and run it
    dvc db downgrade



