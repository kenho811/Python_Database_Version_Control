Change Log
=============

0.1.15
--------

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

- Created docker-compose.yml file for demonstration purposes

- Added Github Action workflows to automate the below:
    - Pushing Docker image (with different tags) and readme to Dockerhub.
    - Pushing the tool to PYPI
