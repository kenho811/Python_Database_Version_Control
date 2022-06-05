Python library to do database version control.

## Usage

### As a Microservice
#### Image on Dockerhub
https://hub.docker.com/repository/docker/kenho811/database-version-control#

- Run the below to see it in action
```commandline
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
```


### As a Commandline tool
#### Commandline tool on PyPI
https://pypi.org/project/database-version-control/

```commandline
# Install the library from PyPi
pip install database-version-control

# To get more instructions of the commandline tool, run the below in the terminal
dvc --help
```

## Documentation
### On Readthedocs (Latest)

https://python-database-version-control.readthedocs.io/en/latest

## Video Demonstration
### On Youtube

- https://www.youtube.com/watch?v=9l3m7zBxN4Y




## Development-Testing-release workflow

```commandline
# Git clone the repo and checkout master
git clone -b master git@github.com:kenho811/Python_Database_Version_Control.git 

# create a feature branch
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

# (By maintainer) For a new release, cut a new release branch with version number (match app version number). 
git checkout -b release/{app_version_number}

```

## CI convention 
- The below is currently triggered via Github Action

Branch | DockerHub tag         | Dockerhub Readme | PyPI version  | Readthedocs version   |
--- |--------------------------|------------------|---------------|-----------------------|
master | latest                | Yes | N/A           | latest                |
feature/{theme} | N/A                   | No | N/A           | N/A                   |
feature/doc | N/A                   | No | N/A           | feature-doc           |
release/{version_num} | release-{version_num} | No | {version_num} | release-{version_num} |



## Details
### Database supported
- Postgres Database


### Database instructions format supported

- SQL files 


#### SQL files naming convention

- All SQL files are considered `revision files`
- They must follow the pattern `RV[0-9]*__.*\.(upgrade|downgrade)\.sql`. In words, it means
  - They start with the prefix `RV`
  - After `RV`, it follows an arbitrary revision number (e.g. RV1, RV2, RV3 etc. etc.)
  - After `RV(arbitrary_revision_number)`, it follows double underscores and an arbitrary number of characters. Everything after `__` describes what the SQL file does.
  - After `RV(arbitrary_revision_number)__(description)`, it follows a dot and the character group of either `upgrade` or `downgrade`. When applied, an upgrade revision file will move the database version upward by 1, while a downgrade revision file will move the database version downward by 1.
  - After `RV(arbitrary_revision_number)__(description).(upgrade/downgrade)`, it follows a dot and the character group of `sql` .
  - Overall, `RV(arbitrary_revision_number)__(description).(upgrade/downgrade).sql`
- Example SQL revision files
  - RV1__create_scm_company_secrets_and_tbl_earnings.upgrade.sql
  - RV1__delete_scm_company_secrets_cascade.downgrade.sql
  - RV2__alter_scm_company_secrets_tbl_earnings_updated_at_add_index.upgrade.sql
  - RV2__alter_scm_company_secrets_tbl_earnings_updated_at_remove_index.downgrade.sql

### Metadata 

- Schema dvc will be created
  - Table dvc.database_revision_history will be created.
  - Table dvc.database_version_history will be created.
  
### User Interface

- CLI
  - Made with Python `Typer` Library
    - Entrypoint is `dvc`
    - Sample commands are
      - `dvc version` --> Show version
      - `dvc cfg` --> Configuration related commands
        - `dvc cfg init` --> Generate configuration files
      - `dvc db` --> Database related commands
        - `dvc db init` --> Initialise the database with metadata schema and tables
        - `dvc db upgrade` ---> Apply Database Upgrade Revision and mark to metadata tables
          - `dvc db upgrade --mark-only` ---> Only mark to metadata tables 
        - `dvc db downgrade` ---> Apply Database Downgrade Revision
          - `dvc db downgrade --mark-only` ---> Only mark to metadata tables 
        - `dvc db current` ---> Current Database Version
        - `dvc db ping` --> Ping database connection
      - `dvc sql` --> SQL related commands
        - `dvc sql generate --from-sql-folder` --> Generate RV files from all SQL files in a given folder
