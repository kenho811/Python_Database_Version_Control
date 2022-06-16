Continuous Integration
=========================

The Codebase is on `github <https://github.com/kenho811/Python_Database_Version_Control>`_.

CI is currently done via github action. It is integrated to the following destinations:

- `Dockerhub <https://hub.docker.com/repository/docker/kenho811/database-version-control#>`_
- `PyPI <https://pypi.org/project/database-version-control/>`_
- `ReadtheDocs (Latest) <https://python-database-version-control.readthedocs.io/en/latest/>`_

The table below shows the details:

.. list-table:: CI convention for branches
   :header-rows: 1

   * - Branch
     - Performs Tests?
     - Artifacts
     - DockerHub Tag
     - Push DockerHub Readme?
     - PyPI Version
     - Readthedocs Version
   * - master
     - Yes
     - Pytest report.
     - latest
     - Yes
     - N/A
     - latest
   * - feature/**
     - Yes
     - N/A
     - N/A
     - No
     - N/A
     - N/A
   * - release/{major.minor}
     - Yes
     - N/A
     - N/A
     - No
     - N/A
     - N/A

.. list-table:: CI convention for tags
   :header-rows: 1

   * - Tag
     - Performs Tests?
     - Artifacts
     - DockerHub Tag
     - Push DockerHub Readme?
     - PyPI Version
     - Readthedocs Version
   * - release/{major.minor.patch}
     - Yes
     - Pytest artifacts + executables in github releases.
     - release-{major.minor.patch}
     - No
     - {majoir.minor.patch}
     - release-major.minor.patch
