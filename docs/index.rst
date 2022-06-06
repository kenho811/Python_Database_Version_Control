.. Database Version Control documentation master file, created by
   sphinx-quickstart on Sun Apr 24 17:21:02 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Database Version Control's  documentation!
=============================================================================



.. image:: _static/img/app_logo_black.png
   :class: center

.. rst-class:: center

   `DVC to version control your database!`


.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :numbered:

   pages/introduction
   pages/quickstart
   usage/index
   design/index
   tests/index
   contribution/index
   pages/changelog

Summary
----------------
Compute (Application) and Storage (Database) are decoupled.

When you make changes to your application code, you should also mke changes to your database.
In other words, you probably want to version control both your application code and your database.
Without version controlling both, any changes in either side can cause incompatibility issues and break the entire service as a whole.

Use DVC now to version control your database!


Description
----------------

Database Version Control (DVC) is a CLI utility which version controls your database in the following ways:

- Generate metadata table(s) in your database;

- For each SQL script applied, update the metadata table(s);

- Exposes the metadata via CLI commands.

Benefits
----------------

- Rich metadata is available in the database. The database can be directly queried with SQL for both historical and current database versions.

- Only plain SQL files are accepted. No extra abstraction layer as is generally available in ORM.


Quick links
~~~~~~~~~~~~~~

* `Code on GitHub <https://github.com/kenho811/Python_Database_Version_Control>`_
* `Docker Image on Dockerhub <https://hub.docker.com/repository/docker/kenho811/database-version-control#>`_
* `Documentation on Readthedocs (latest) <https://python-database-version-control.readthedocs.io/en/latest>`_
* `Demo on Youtube <https://www.youtube.com/watch?v=9l3m7zBxN4Y>`_


Test Status
~~~~~~~~~~~~~~
* `Pytest Report <../_static/pytest/report.html>`_


.. warning::
   As of 5th June 2022, only `Postgresql` is supported.

   Support for other databases will be added in the future. Stay tuned!
