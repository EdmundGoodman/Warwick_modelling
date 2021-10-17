Example Usage
=============

Importing the module
--------------------

.. code-block:: python

    """Import all assets for the model"""
    from tiered_antibiotic_resistance_model import *


Running the model
-----------------

.. code-block:: python

    """Run and draw a graph of the model with the default parameters"""
    run_and_output()


Changing parameters and settings in-line
----------------------------------------

.. code-block:: python

    """Change the number of timesteps parameter and the graph type setting,
    then run the model"""
    Params.NUM_TIMESTEPS = 100
    Settings.GRAPH_TYPE = "stackplot"
    run_and_output()
