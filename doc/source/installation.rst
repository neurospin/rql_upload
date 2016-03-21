

.. _install_guid:

=======================
Installing `RQL Upload`
=======================

This tutorial will walk you through the process of installing RQL Upload:

    * **rql_upload**: a cube that can only be instanciated
      if `cubicweb is installed <https://docs.cubicweb.org/admin/setup>`_.


.. _install_rqlupload:

Installing rql_upload
=====================

Installing the current version
------------------------------

Install from *github*
~~~~~~~~~~~~~~~~~~~~~

**Clone the project**

>>> cd $CLONEDIR
>>> git clone https://github.com/neurospin/rql_upload.git

**Update your CW_CUBES_PATH**

>>> export CW_CUBES_PATH=$CLONE_DIR/rql_upload:$CW_CUBES_PATH

Make sure the cube is in CubicWeb's path
----------------------------------------

>>> cubicweb-ctl list

Create an instance of the cube and configure the demo upload service
--------------------------------------------------------------------

>>> cubicweb-ctl create rql_upload toy_upload

When asked, specify a directory path where the uploaded file will be stored:

>>> rql_upload options
>>> ------------------
>>> :upload_directory:
>>> base directory in which a the files are uploaded.
>>> (default: ):

And the json file that will define your forms:

>>> :upload_structure_json:
>>> json file describing the different upload entities.
>>> (default: ):

An example of configuration file can be found within the cubes file:

>>> $CLONE_DIR/rql_upload/demo/demo.json

You can then run the instance in debug mode:

>>> cubicweb-ctl start -D toy_upload

The last line of the prompt will indicate which url the 
instance can be reached by:

>>> (cubicweb.twisted) INFO: instance started on http://url:port/

Change configuration
--------------------

You can change to configuration by modifying the instance configuration file
stored on your system:

>>> ...etc/cubicweb.d/toy_upload/all-in-one.conf
