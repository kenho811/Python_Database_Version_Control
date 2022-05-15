Python library to do database version control.

## PyPi

See: https://pypi.org/project/database-version-control/

## Demonstration

See: https://www.youtube.com/watch?v=9l3m7zBxN4Y


## Usage

1. Git clone the repository. Cd into the repository.
2. pip install with `pip install .`
3. Run `dvc --help` in the terminal to see further instructions.

## Development

1. Git clone the repository. Cd into the repository.
2. pip install with `pip install .[dev]` (in zsh, do `pip install .'[dev]'`)
3. use `pytest` to run tests

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
      - `dvc cfg init` --> Generate configuration files
      - `dvc db init` --> Initialise the database with metadata schema and tables
      - `dvc db upgrade` ---> Apply Database Upgrade Revision and mark to metadata tables
        - `dvc db upgrade --mark-only` ---> Only mark to metadata tables 
      - `dvc db downgrade` ---> Apply Database Downgrade Revision
        - `dvc db downgrade --mark-only` ---> Only mark to metadata tables 
      - `dvc db current` ---> Current Database Version
      - `dvc db ping` --> Ping database connection
