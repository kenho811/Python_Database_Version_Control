Quickstart
=============


Docker Image
-------------

.. note::
    The tool is containerised and is distributed on `Dockerhub <https://hub.docker.com/repository/docker/kenho811/database-version-control#>`_

    Check out the `docker-compose.yml` file in `the github repository <https://github.com/kenho811/Python_Database_Version_Control>`_ to run a demo!


Run the below to see it in action.

.. code-block:: rst

    # Clone the repo and checkout release branch
    git clone -b release git@github.com:kenho811/Python_Database_Version_Control.git

    # cd to the repository
    cd Python_Database_Version_Control

    # Fnd the docker-compose.yml and run
    docker compose up

    # Using psql as client, access the postgres DB and see the result
    (URL: postgres://test:test@localhost:5433/test)
    PGPASSWORD=test psql -U test -d test -h localhost -p 5433

    # Check out docker-compose.yml file for usage as a microservice

See detailed usage of the `Docker Image <../usage/dockerimage.html>`_

PyPI Library
------------

.. note::
    The commandline tool is uploaded to `PyPI <https://pypi.org/project/database-version-control/>`_


Run the below to see it in action.

.. code-block:: rst

    # Install the library from PyPi
    pip install database-version-control

    # To get more instructions of the commandline tool, run the below in the terminal
    dvc --help


See detailed usage of the `commandline tool <../usage/cli.html>`_
