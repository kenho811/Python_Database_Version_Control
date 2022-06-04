Continuous Integration
=========================

The Codebase is on `github <https://github.com/kenho811/Python_Database_Version_Control>`_.

CI is currently done via github action. It is integrated to the following destinations:

- `Dockerhub <https://hub.docker.com/repository/docker/kenho811/database-version-control#>`_
- `PyPI <https://pypi.org/project/database-version-control/>`_
- `ReadtheDocs <https://pypi.org/project/database-version-control/>`_

The table below shows the details:

.. list-table:: CI convention
   :header-rows: 1

   * - Branch
     - Performs Tests?
     - DockerHub Tag
     - PyPI Version
     - Readthedocs Version
   * - master
     - Yes
     - latest
     - N/A
     - latest
   * - feature/{theme}
     - Yes
     - N/A
     - N/A
     - N/A
   * - release/{version}
     - Yes
     - release-{version}
     - {version}
     - N/A
