Change Log
=============

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
