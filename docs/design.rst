Design
=======

.. warning::

    (Still work in progress)

This section explains the internal structural design of the tool.


.. graphviz::
   :name: Database Verion Control Tool Setup
   :caption: Internal structure
   :alt: How Sphinx and GraphViz Render the Final Document
   :align: center

   digraph foo {
      graph [fontname="Verdana", fontsize="12"];
      node [fontname="Verdana", fontsize="12"];
      edge [fontname="Sans", fontsize="9"];


      # Define classes
      dvc_cli [label="DVC CLI", shape="rect"];
      ConfigReader [label="ConfigReader", shape="class"];
      ConfigFileWriter [label="ConfigFileWriter", shape="class"];

      # Define Environment


      dvc_cli
      "Env Var" -> ConfigReader -> "baz";
      ConfigFileWriter -> "Config File" -> ConfigReader -> "baz";


   }


.. graphviz::
    :name: sphinx.ext.graphviz
    :caption: Sphinx and GraphViz Data Flow
    :alt: How Sphinx and GraphViz Render the Final Document
    :align: center

     digraph "sphinx-ext-graphviz" {
         size="6,4";
         rankdir="LR";
         graph [fontname="Verdana", fontsize="12"];
         node [fontname="Verdana", fontsize="12"];
         edge [fontname="Sans", fontsize="9"];

         sphinx [label="Sphinx", shape="component",
                   href="https://www.sphinx-doc.org/",
                   target="_blank"];
         dot [label="GraphViz", shape="component",
              href="https://www.graphviz.org/",
              target="_blank"];
         docs [label="Docs (.rst)", shape="folder",
               fillcolor=green, style=filled];
         svg_file [label="SVG Image", shape="note", fontcolor=white,
                 fillcolor="#3333ff", style=filled];
         html_files [label="HTML Files", shape="folder",
              fillcolor=yellow, style=filled];

         docs -> sphinx [label=" parse "];
         sphinx -> dot [label=" call ", style=dashed, arrowhead=none];
         dot -> svg_file [label=" draw "];
         sphinx -> html_files [label=" render "];
         svg_file -> html_files [style=dashed];
     }


.. graphviz::

    graph {
      "1.5x0.5" [shape=rect margin="1.5,0.5"] # in inches
      "0.5x1.5" [shape=rect margin="0.5,1.5"] # in inches
      "1.5x1.5" [shape=rect margin="1.5"]     # in inches
    }