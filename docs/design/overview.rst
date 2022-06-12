Overview
==========

This page explains gives a graphical overview of the tool.



DVC CLI commands and subcommands
----------------------------------

This section explains the client-facing side of the tool. The library is exposed via the commandline `dvc`.


.. graphviz::
   :name: Database Verion Control CLI Commands and Subcommands
   :caption: DVC CLI Commands and Subcommands
   :align: center

   digraph cli {
      graph [fontname="Verdana", fontsize="12"];
      node [fontname="Verdana", fontsize="12"];
      edge [fontname="Sans", fontsize="9"];
      rankdir="LR";

     dvc -> {cfg, db, sql}
     cfg -> init
     db -> {ping, init, upgrade, downgrade}
     sql -> generate


   }

Core Structure
----------------------

This section explains the core of the tool. It shows the interaction between the classes (marked in `yellow`). Greyed out items are features yet to be implemented.

.. graphviz::
   :name: Database Verion Control Core Structure
   :caption: DVC Core structure
   :align: center


   digraph core {
      graph [fontname="Verdana", fontsize="12"];
      node [fontname="Verdana", fontsize="12"];
      edge [fontname="Sans", fontsize="9"];
      label = "Core";

      env [label="Env Var"];
      conffile [label="Config File"];
      ConfigReader [label="ConfigReader", shape="class", color="yellow", style="filled"];
      ConfigFileWriter [label="ConfigFileWriter", shape="class", color="yellow", style="filled"];
      DatabaseRevisionFilesManager [label="DatabaseRevisionFilesManager", shape="class", color="yellow", style="filled"];
      sqlfiles [label="SQL Files"];


      subgraph cluster_0 {
          label="SQLFileExecutors and Databases"

          PostgresqlSQLFileExecutor[shape="class", color="yellow", style="filled"];
          MysqlSQLFileExecutor[shape="class", color="grey", style="filled"];
          BigquerySQLFileExecutor[shape="class", color="grey", style="filled"];
          postgresql
          mysql[color=grey, style="filled"];
          bigquery[color=grey, style="filled"];

          PostgresqlSQLFileExecutor -> postgresql[label="apply"]
          MysqlSQLFileExecutor -> mysql[label="apply"]
          BigquerySQLFileExecutor -> bigquery[label="apply"]
      }

      env -> ConfigReader[label="input"];
      ConfigFileWriter -> conffile[label="generate"];
      conffile -> ConfigReader[label="input"];
      ConfigReader -> DatabaseRevisionFilesManager[label="input"];
      DatabaseRevisionFilesManager -> sqlfiles[label="lookup"];
      DatabaseRevisionFilesManager -> {PostgresqlSQLFileExecutor,MysqlSQLFileExecutor,BigquerySQLFileExecutor}[label="call"];

      }
