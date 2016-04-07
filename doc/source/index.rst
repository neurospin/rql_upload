..  NSAp documentation master file, created by
    sphinx-quickstart on Wed Sep  4 12:18:01 2013.
    You can adapt this file completely to your liking, but it should at least
    contain the root `toctree` directive.


RQL Upload
==========

Summary
-------

* Propose a cube to create an upload service from a json file description.
* Contain a demonstrator that can be generated from scratch.

Description
-----------

Cube to upload data in a cubicweb CWUpload entity. This cube has no dependency
on other cubes.
The :ref:`database schema <schema_ref>` has been modified to store form
parameters in the database and to deport file on the server file system.
Some :ref:`navigation views <views_nav>` are designed to simplify the access
to the :ref:`desired forms <views_form>`. 

|

Contents
========
.. toctree::
    :maxdepth: 1

    installation
    documentation


Search
=======

:ref:`search`
