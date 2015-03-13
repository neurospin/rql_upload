
.. _install_guid:

=========================
Installing `Rql Upload`
=========================

This tutorial will walk you through the process of installing Rql Upload...

  * :ref:`Install an official release <install_release>`: this
    is the best approach for users who want a stable version.


.. _install_release:

Installing a stable version and runing the example
==================================================


Get the cube from *github*
--------------------------

* Clone the project: git clone https://github.com/neurospin/rql_upload.git
* Update your PYTHONPATH: export PYTHONPATH=$CLONE_DIR:PYTHONPATH

Make sure the cube is in CubicWeb's path
----------------------------------------

>>> cubicweb-ctl list

if the cube is not is the displayed list, update your CW_CUBES_PATH environment
variable.

Create an instance of the cube and run the example
--------------------------------------------------

>>> cubicweb-ctl create rql_upload myUploadInstance

When asked, specify a directory path where the file will be stored:

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

<cube_directory>/example/example.json

You can then run the instance

>>> cubicweb-ctl start -D myUploadInstance

The last line of the prompt will indicate which url the 
instance can be reached by:

>>> (cubicweb.twisted) INFO: instance started on http://url:port/


Change configuration file
=========================

If you want to create your own forms,  you can either make modification in the
example file (not recommanded) or you can create your own configuration file.

Replace the upload_structure_json variable in the all-in-one.conf file.

>>> ...etc/cubicweb.d/myUploadInstance/all-in-one.conf
