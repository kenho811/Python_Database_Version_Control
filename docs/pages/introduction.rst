Introduction
=============

.. warning::

    (Still work in progress)

What is Version Control?
------------------------

In its most general sense, Version Control means to track and manage the different versions of a document or set of documents.
While it is mostly practised in the world of software engineering, its use cases also abound in other areas.
For instance, book writers often benefit from version controlling their drafts. This enables them to explore different writing styles, themes and so on. Failed attempt in a certain direction can be safely scrapped while the writer jumps back to the version he is most comfortable in.
What is Software Version Control?
As mentioned, software engineering practices version control heavily. Unlike hardware, software has high malleability. This makes it necessary to keep track of the changes made to the software and to have the ability to jump back to the prior version when the latest version breaks.
The current industry standard for Software Version Control is Git, a distributed version control system created by Linux Torvald. It has superseded its predecessors like SVN, which is a local version control system which stores a project's history in a single server.
What is Database Version Control?
Interestingly, while there is much discussion around Software Version Control, there seems to be a lack of discussion around database version control.
Database, especially Relational Database Management System (RDBMS), does not merely store data. It also stores, among others, data about data (metadata, like DDL) and user access privileges (DCL),
Given that a lot of applications are data-driven, which means the software's behaviour is affected by the data which it receives, version controlling your database should not come off as secondary to version controlling your software.
Examples of Existing Database Version Control Systems in the market

Existing Database Version Control Tools
--------------------------------------------
There are a number of existing database version control tools.

Commercial
~~~~~~~~~~
Examples which are commericial and written in java.

- `flyway <https://flywaydb.org/>`_
- `liquibase <https://www.liquibase.org/>`_

Open Source
~~~~~~~~~~~

In the python world, we have the below open-source products.

- `alembic <https://alembic.sqlalchemy.org/en/latest/>`_
- `yoyo-migration <https://ollycope.com/software/yoyo/latest/>`_

Personal Experience with existing tools
--------------------------------------------
Shortcomings of existing Database Version Control systems in python

I have experimented with both alembic and yoyo-migration, but found the following shortcomings:
alembic: The metadata is mostly stored as files in the repository, and NOT as an entry in the database. It makes it difficult to know the database version by running SQL.
yoyo-migration: The SQL migration files must be prefixed with numbers left padded with zeros. For instance, '0001__description.sql'. If we have more than 1000 SQL files, then we probably need to rename the old files (e.g. to '00001__descrition.sql'). However, given that file names must be immutable in order for the database version control system to work properly, it means that it always has a upper limit as to how many SQL migration files you can have.
This makes me want to create my own version of database version control system (DVC).
My own database version control system in python: Design Requirements
My goal is to have a DVC satisfying the below requirements:
It works only with the Postgresql database (Optionally, it should be extendable)
It accepts only SQL files (It does not use ORM, like SQLalchemy)
It retains rich metadata in the database, so that we can check the database version via SQL.
The spirit is that the DVC should act like `git`, which stores all the git objects in a `.git` folder. Similarly, there should be a table in the database, which stores all the metadata of the DVC, such that a simple SQL can be used to query the database version.

