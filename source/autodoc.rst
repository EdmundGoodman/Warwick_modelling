.. role:: raw-html(raw)
    :format: html


Interface
=========

.. automodule:: model


The run function
----------------

.. autofunction:: run


The run_and_output function
---------------------------

.. autofunction:: run_and_output


Infection object
----------------

.. autoclass:: Infection
    :members:
    :private-members:
    :special-members:


Treatment object
----------------

.. autoclass:: Treatment
    :members:
    :private-members:
    :special-members:


Person object
-------------

.. autoclass:: Person
    :members:
    :private-members:
    :special-members:


Model object
------------

.. autoclass:: Model
    :members:
    :private-members:
    :special-members:


DataHandler object
------------------

.. autoclass:: DataHandler
    :members:
    :private-members:


DataRenderer object
-------------------

.. autoclass:: DataRenderer
    :members:
    :private-members:


Params object
-------------

.. autoclass:: Params

    .. automethod:: reset_granular_parameters

    .. autoattribute:: NUM_TIMESTEPS
    .. autoattribute:: POPULATION_SIZE
    .. autoattribute:: INITIALLY_INFECTED
    .. autoattribute:: DRUG_NAMES
    .. autoattribute:: PROBABILITY_MOVE_UP_TREATMENT
    .. autoattribute:: TIMESTEPS_MOVE_UP_LAG_TIME
    .. autoattribute:: ISOLATION_THRESHOLD
    .. autoattribute:: PRODUCT_IN_USE
    .. autoattribute:: PRODUCT_DETECTION_LEVEL
    .. autoattribute:: PROBABILITY_GENERAL_RECOVERY
    .. autoattribute:: PROBABILITY_TREATMENT_RECOVERY
    .. autoattribute:: PROBABILITY_MUTATION
    .. autoattribute:: PROBABILITY_DEATH
    .. autoattribute:: DEATH_FUNCTION
    .. autoattribute:: PROBABILITY_SPREAD
    .. autoattribute:: NUM_SPREAD_TO
    .. autoattribute:: DRUG_PROPERTIES
    .. autoattribute:: NUM_RESISTANCES
    .. autoattribute:: RESISTANCE_PROPERTIES


Settings object
---------------

.. autoclass:: Settings

    .. autoattribute:: RANDOM_SEED
    .. autoattribute:: REPORT_PROGRESS
    .. autoattribute:: REPORT_PERCENTAGE
    .. autoattribute:: REPORT_MOD_NUM
    .. autoattribute:: PRINT_DATA
    .. autoattribute:: OUTPUT_PADDING
    .. autoattribute:: DRAW_GRAPH
    .. autoattribute:: GRAPH_TYPE
    .. autoattribute:: EXPORT_TO_EXCEL
    .. autoattribute:: DEFAULT_EXCEL_FILENAME
