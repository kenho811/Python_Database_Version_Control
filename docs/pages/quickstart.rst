Quickstart
=============

Executable
--------------
.. note::
    Executables are available on `Github Releases <https://github.com/kenho811/Python_Database_Version_Control/releases>`_


- The releases page provides executables on the below three Operating Systems.

  - Mac (Latest)

  - Linux Ubunutu (Latest)

  - Windows (Latest)

if you happen to use one of the OSes listed above, you can download the executable directly and use it without installing python!

PyPI Library
---------------

.. note::
    The commandline tool is uploaded to `PyPI <https://pypi.org/project/database-version-control/>`_


Run the below to see it in action.

.. code-block:: rst

    # Install the library from PyPi
    pip install database-version-control

    # To get more instructions of the commandline tool, run the below in the terminal
    dvc --help


See detailed deployment of the `commandline tool <../deployment/cli.html>`_

Docker Image
-------------

.. note::
    The tool is containerised and is distributed on `Dockerhub <https://hub.docker.com/repository/docker/kenho811/database-version-control#>`_

    Check out the `docker-compose.yml` file in `the github repository <https://github.com/kenho811/Python_Database_Version_Control>`_ to run a demo!


Run the below to see it in action.

.. code-block:: bash

    # Clone the repo and checkout release branch
    git clone git@github.com:kenho811/Python_Database_Version_Control.git

    # cd to the repository
    cd Python_Database_Version_Control/docker_compose_demo

    # Fnd the docker-compose.yml and run
    docker compose up

    # Using psql as client, access the postgres DB and see the result
    (URL: postgres://test:test@localhost:5433/test)
    PGPASSWORD=test psql -U test -d test -h localhost -p 5433

    # Check out docker-compose.yml file for usage as a microservice

See detailed deployment of the `Docker Image <../deployment/dockerimage.html>`_



