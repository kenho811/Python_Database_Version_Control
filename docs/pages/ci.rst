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
     - Generate any artifacts?
     - DockerHub Tag
     - Push DockerHub Readme?
     - PyPI Version
     - Readthedocs Version
   * - master
     - Yes
     - Yes. Pytest artifacts.
     - latest
     - Yes.
     - N/A
     - latest
   * - feature/{theme}
     - Yes
     - N/A
     - N/A
     - No
     - N/A
     - N/A
   * - release/{version}
     - Yes
     - Yes. Pytest artifacts.
     - release-{version}
     - No
     - {version}
     - N/A
