
.. _example :

Example
=======

This page describes the example model design and how to setup and run the example.


.. index:: tutorial
.. index:: example

Example Model Design
--------------------

...


Setup
-----

The following describes the example model setup.


Folder and File Setup
~~~~~~~~~~~~~~~~~~~~~

The example has the following root folder/file setup:

  * configs - settings, expressions files, etc.
  * data - input data such as land use, synthetic population files, and skims
  * output - outputs folder
  * run_asimtbm.py - main script to run the model

Inputs
~~~~~~

In order to run the example, you first need two input files in the ``data`` folder as identified in the ``configs\settings.yaml`` file:

* skims_file: skims.omx - an OMX matrix file containing the MTC travel model one skim matrices for a subset of zones.

.. note::

  Input files can be viewed with the `OMX Viewer <https://github.com/osPlanning/omx/wiki/OMX-Viewer>`__.

Configuration
~~~~~~~~~~~~~

The ``configs`` folder contains settings, expressions files, and other files required for specifying
model utilities and form.  The first place to start in the ``configs`` folder is ``settings.yaml``, which
is the main settings file for the model run.  This file includes:

* ``models`` - list of model steps to run - auto ownership, tour frequency, etc. - see :ref:`model_steps`
* ``trace_od`` - trace origin, destination pair in accessibility calculation; comment out for no trace
* ``output_tables`` - list of output tables to write to CSV

Logging
~~~~~~~

Included in the ``configs`` folder is the ``logging.yaml``, which configures Python logging
library.

Refer to the :ref:`tracing` section for more detail on tracing.

.. _model_steps :

Pipeline
~~~~~~~~

The ``models`` setting contains the specification of the data pipeline model steps, as shown below:

::

 models:
    - destination_choice
    - write_data_dictionary
    - write_tables

These model steps must be registered orca steps, as noted below.  If you provide a ``resume_after``
argument to :func:`activitysim.core.pipeline.run` the pipeliner will load checkpointed tables from the checkpoint store
and resume pipeline processing on the next model step after the specified checkpoint.

::

  resume_after = None
  #resume_after = 'destination_choice'

The model is run by calling the :func:`activitysim.core.pipeline.run` method.

::

  pipeline.run(models=_MODELS, resume_after=resume_after)

Running the Example
-------------------

To run the example, do the following:

* Open a command line window in the ``example`` folder
* Activate the correct conda environment if needed
* Run ``python run_asimtbm.py`` to run the data pipeline (i.e. model steps)
* ActivitySim should log some information and write outputs to the ``output`` folder.

The example should complete within a couple seconds since it is running a small sample of households.


Outputs
-------

The key output of ActivitySim is the HDF5 data pipeline file ``outputs\pipeline.h5``.  This file contains a copy
of each key data table after each model step in which the table was modified.  The
``scripts\make_pipeline_output.py`` script uses the information stored in the pipeline file to create the table
below for a small sample of households.  The table shows that for each table in the pipeline, the number of rows
and/or columns changes as a result of the relevant model step.  A ``checkpoints`` table is also stored in the
pipeline, which contains the crosswalk between model steps and table states in order to reload tables for
restarting the pipeline at any step.

The example ``simulation.py`` run model script also writes the final tables to CSV files
for illustrative purposes by using the :func:`activitysim.core.pipeline.get_table` method via the ``write_tables`` step.
This method returns a pandas DataFrame, which can then be written to a CSV with the ``to_csv(file_path)`` method.

ActivitySim also writes log and trace files to the ``outputs`` folder.  The activitysim.log file,
which is the overall log file is always produced.  If tracing is specified, then trace files are
output as well.

.. _tracing :

Tracing
~~~~~~~

If an OD pair trace is specified, then ActivitySim will output the segment calculations trace
files:

* ``trace.od_table.csv`` - impedance expression results for the OD pair.
* ``trace.segment_od_<segment_name>.csv`` - impedance expression results for each segment.

With the set of output CSV files, the user can trace ActivitySim calculations in order to ensure they are correct and/or to
help debug data and/or logic errors.
