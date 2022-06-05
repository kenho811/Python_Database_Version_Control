.. Database Version Control documentation master file, created by
   sphinx-quickstart on Sun Apr 24 17:21:02 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Database Version Control Version documentation!
=============================================================================

.. note::
   See latest test report: `here <_static/pytest/report.html>`_



.. toctree::
   :maxdepth: 2
   :caption: Contents:
   :numbered:

   pages/introduction
   pages/quickstart
   design/index
   tests/index
   workflow/index
   pages/changelog


Summary
----------------

Database Version Control (DVC) is a CLI utility which version controls your database in the following ways:

- Generate metadata table(s) in your database;

- For each SQL script applied, update the metadata table(s);

- Exposes the metadata via CLI commands.


Quick links
~~~~~~~~~~~~~~

* `Code on GitHub <https://github.com/kenho811/Python_Database_Version_Control/tree/release>`_
* `Docker Image on Dockerhub <https://hub.docker.com/repository/docker/kenho811/database-version-control#>`_
* `Documentation on Readthedocs (latest) <https://python-database-version-control.readthedocs.io/en/latest>`_
* `Demo on Youtube <https://www.youtube.com/watch?v=9l3m7zBxN4Y>`_


.. warning::
   As of 5th June 2022, only `Postgresql` is supported.

   Support for other databases will be added in the future. Stay tuned!
