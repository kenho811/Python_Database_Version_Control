Overview
============

Command Line Interface
-------------------------

.. image:: ../_static/gif/command_line_interface.gif
   :class: center
   :alt: Command Line Interface

- Showing CLI commands.


Rich Database Metadata
-------------------------

.. note::
    More information about the metadata can be found under `design/metadata <../design/metadata.html>`_

.. image:: ../_static/gif/rich_metadata.gif
   :class: center
   :alt: Rich Metadata

- Showing the metadata tables.
    - dvc.database_revision_history table which shows the revision SQL files applied.
    - dvc.database_version_history table which shows the database version which results from the revision SQL files applied.


Upgrade or Downgrade
----------------------

.. image:: ../_static/gif/database_upgrade_and_downgrade.gif
   :class: center
   :alt: Rich Metadata

- Showing upgrade and downgrade command.
    - Started from database version 1 (Shown via `dvc db current`)
    - Showed the Revision SQL files under the default folder `sample_revision_sql_files`.
    - Applied database upgrade via `dvc db upgrade`.
    - Showed the database version became 2.
    - Applied database downgrade via `dvc db downgrade`.
    - Showed the database version was back to 1.

Flexible Configuration Format
--------------------------------------

Configuration is read either from i. Configuration File (config.yaml) or ii. Environment Variable

Configuration File
~~~~~~~~~~~~~~~~~~~~

.. note::
   The configuration file template can be generated via `dvc cfg init`

.. image:: ../_static/gif/config_via_config_file.gif
   :class: center
   :alt: Config Via Configuration File

- Showing dvc tool reads configuration from a configuration file.
    - Ran a postgres DB via docker `docker run -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5433:5432 postgres:latest`
    - Copied a `config.yaml` file with configurations which match the spun up postgres DB.
    - Pinged the DB with `dvc db ping`. Success!

- The config.yaml file looks as follows:

.. literalinclude:: ../_static/files/sample_config.yaml




Environment Variable
~~~~~~~~~~~~~~~~~~~~~~~

.. note::
   The names of the environment variables can be found in the `docker compose file <https://github.com/kenho811/Python_Database_Version_Control/blob/master/docker-compose.yml#L21-L27>`_

.. image:: ../_static/gif/config_via_env_var.gif
   :class: center
   :alt: Config Via Env Var

- Showing dvc tool reads configuration from environment variables
    - Ran a postgres DB via docker `docker run -e POSTGRES_USER=test -e POSTGRES_PASSWORD=test -e POSTGRES_DB=test -p 5433:5432 postgres:latest`
    - Loaded the env variables to the shell.
    - Pinged the DB with `dvc db ping`. Success!

- The environment variables look as follows:


.. literalinclude:: ../_static/files/sample_env_var.log
   :language: bash
