Change Log
=============

0.4.1
--------
- Added --dry-run to both `dvc db upgrade` and `dvc db downgrade`. When set to True, the CLI will stop before the execution of SQL files
- Added tests for DatabaseRevisionFilesManager for i. getting files by pointer and ii. getting files by steps.
- Added option to change logging level in config file and env variables
- Added demo files and step-by-step guide under in the `feature pages <../feature/guide.html>`_

0.4.0
--------
- Added dynamic generation of src package and tests package documentation in docs with sphinx-apidoc.
- Added --head to `dvc db upgrade` and --base `dvc db downgrade` respectively



0.3.3
--------
- Added CI testing for binaries generated for 3 Oses. For Windows, Ubuntu Linux and Mac, run the below in the CI pipeline:

    - Build binary
    - Run postgres server. Run all DVC commands against it.
    - Push to Github release

0.3.2
--------
- Included ./setup.cfg to Dockerfile. Fixed missing .sql files in Docker Image to Dockerhub

0.3.1
--------
- Moved `package_data` to setup.cfg. Fixed missing .sql files in PyPI.

0.3.0
--------
- Added --steps and --confirm flags to `dvc db upgrade` and `dvc db downgrade`
- Added dunder methods for the below classes:
    - __le__, __gr__, __eq__ for DatabaseRevisionFile
    - __add__, __sub__, __eq__ for DatabaseVersion
- Codified the below relationship with dunder methods:
    - `DatabaseVersion - DatabaseVersion = [DatabaseRevisionFiles]`
    - `DatabaseVersion + DatabaseRevisionFile = DatabaseVersion`
- Removed `dvc sql generate`, as that is Files System related.
- Added diagram to illustrate DatabaseVersion and DatabaseRevisionFile


0.2.1
--------
- Refactored Github workflows. Separated the below components from Github Workflows
    - Running pytest
    - Building and pushing python library to PyPI
    - Building and Pushing artifacts to Readthedocs
    - Building and pushing to Dockerhub
    - Building and pushing Linux, Mac and Windows binaries to Github Releases

0.2.0
--------
- Included help text and documentation URL in the CLI.
- Followed SemVer more closely. Bumped minor version with added feature and bump patch for bug fixes. Switched to using tag (not branch) for releases.


0.1.16
--------
- Created binaries for windows, mac and linux with pyinstaller. added sql files to the binaries.

- Removed confirmation for both upgrade and downgrade command (i.e. `dvc db upgrade` and `dvc db downgrade`)



0.1.15
--------

- Update Dockerfile. Changed instruction ``CMD`` to ``ENTRYPOINT`` for ``dvc`` command.

- Added pages to documentation using sphinx

- Created graphs using graphviz and dots

- Added Github Action workflows to automate the below:
    - generating pytest report artifacts
    - pushing both artifacts and .rst files to Readtheedocs for building documentation


0.1.14
--------

- Created ConfigReader, ConfigFileWriter and other objects to hold states.

- Added the option to pass configuration as environment variables.

- Added unit tests and integrations tests (for postgres)

- Created Dockerfile to containerise the tool

- Created docker-compose.yml file for demonstration purposes. Created demo_assets to be attached as volume to docker-compose containers.

- Added Github Action workflows to automate the below:
    - Pushing Docker image (with different tags) and readme to Dockerhub.
    - Pushing the tool to PYPI
