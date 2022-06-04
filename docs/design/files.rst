Files
=======

The tool discovers and applies SQL files to the database for version control.

These files need to follow a certain naming conventions.


.. SQL files naming convention::

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
