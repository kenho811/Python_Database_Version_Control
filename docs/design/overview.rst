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

     dvc -> {cfg, db}
     cfg -> {init, show}
     db -> {ping, init, upgrade, downgrade}


   }

Data Structures
-------------------------------------------------

Core Structure
~~~~~~~~~~~~~~~~

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


DatabaseVersion and DatabaseRevisionFile
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

- Below is a series of graphs illustrating the relationship between

    - Current Database Version (DatabaseVersion)

    - Target Database Version  (DatabaseVersion)

    - One or more Database Revision Files (DatabaseRevisionFiles)

.. graphviz::
   :name: Current Database Version V1 plus Database Revision File RV2 Upgrade equqls Target Database Version V2
   :caption: V1 + RV2 (Upgrade) = V2



   digraph core {
      rankdir="LR";

      curr_dbver [label="V1", shape="cylinder"];
      tar_dbver [label="V2", shape="cylinder"];
      dbrev_file [label="RV2, Upgrade", shape="note"];

      subgraph cluster_0 {

          {rank=same curr_dbver dbrev_file}

          curr_dbver -> dbrev_file[label="plus", arrowhead="none"];

      }

      dbrev_file -> tar_dbver [ltail=cluster_0, lhead=tar_dbver];

      }

.. graphviz::
   :name: Current Database Version V1 plus Database Revision File RV1 Downgrade equals Target Database Version V0
   :caption: V1 + RV1 (Downgrade) = V0


   digraph core {
      rankdir="LR";

      curr_dbver [label="V1", shape="cylinder"];
      tar_dbver [label="V0", shape="cylinder"];
      dbrev_file [label="RV1, Downgrade", shape="note"];

      subgraph cluster_0 {

          {rank=same curr_dbver dbrev_file}

          curr_dbver -> dbrev_file[label="plus", arrowhead="none"];

      }

      dbrev_file -> tar_dbver [ltail=cluster_0, lhead=tar_dbver];

      }

.. graphviz::
   :name: Target Database Version V5 minus Current Database Version V3 gives RV4 Upgrade and RV5 Upgrade
   :caption: V5 - V3 = [RV4 Upgrade + RV5 Upgrade]


   digraph core {
      rankdir="LR";

      curr_dbver [label="V3", shape="cylinder"];
      tar_dbver [label="V5", shape="cylinder"];
      dbrev_file_1 [label="RV4, Upgrade", shape="note"];
      dbrev_file_2 [label="RV5, Upgrade", shape="note"];

      subgraph cluster_0 {

          {rank=same curr_dbver tar_dbver}

          tar_dbver -> curr_dbver[label="minus", arrowhead="none"];

      }

      subgraph cluster_ {

          {rank=same dbrev_file_1 dbrev_file_2}

          dbrev_file_1 -> dbrev_file_2[ arrowhead="none"];

      }

      curr_dbver -> dbrev_file_1 [ltail=cluster_0, lhead=cluster_1];

      }

.. graphviz::
   :name: Target Database Version V3 minus Current Database Version V5 gives RV5 Downgrade and RV4 Downgrade
   :caption: V3 - V5 = [RV5 Downgrade + RV4 Downgrade]


   digraph core {
      rankdir="LR";

      curr_dbver [label="V5", shape="cylinder"];
      tar_dbver [label="V3", shape="cylinder"];
      dbrev_file_1 [label="RV5, Downgrade", shape="note"];
      dbrev_file_2 [label="RV4, Downgrade", shape="note"];

      subgraph cluster_0 {

          {rank=same curr_dbver tar_dbver}

          tar_dbver -> curr_dbver[label="minus", arrowhead="none"];

      }

      subgraph cluster_ {

          {rank=same dbrev_file_1 dbrev_file_2}

          dbrev_file_1 -> dbrev_file_2[ arrowhead="none"];

      }

      curr_dbver -> dbrev_file_1 [ltail=cluster_0, lhead=cluster_1];

      }
