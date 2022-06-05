Development
==============

This page explains the development workflow.

Contributors
---------------

.. code-block:: rst

    # Git clone the repo and checkout master
    git clone -b master git@github.com:kenho811/Python_Database_Version_Control.git

    # create a feature branch from the master branch
    git checkout -b feature/{code_change_theme}

    # Pip install dependencies
    pip install with `pip install ".[dev]"`

    # Enable local githooks
    git config --local core.hooksPath .githooks/

    # Development

    # Write unit + integration tests

    # Run pytest
    pytest

    # Generate Documentation locally. ISLOCAL=1 removes local dependencies.
    cd docs
    ISLOCAL=1 make clean html

    # Open PR against master


Maintainers
-----------

.. code-block:: rst

    # Review and merge PR into master branch

    # Update local master branch
    git checkout master
    git pull

    # Update the tool's version under src/dvc/version.py
    # See: https://github.com/kenho811/Python_Database_Version_Control/blob/master/src/dvc/version.py#L1
    # Example: __version__ = "{new_version_num}"

    # Cut a release branch with the same updated version number
    git checkout -b release/{new_version_num}
    git push --set-upstream origin release/{new_version_num}


- The CI pipeline specified `here <ci.html>`_ will manage the rest.