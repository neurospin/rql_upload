:orphan:

.. _schema_ref:

####################
Schema modifications
####################

Description
-----------
The database schema has been modified and a CWUpload entity has been added.
When an upload request is processed, a CWUpload entity is created. This latter is
responsible to store the inline form parameters in an 'UploadForm' entity and the
files in a deported 'UploadFile' entity.

.. _schema_api:

:mod:`rql_upload`: Schema
-------------------------

.. currentmodule:: rql_upload

.. autosummary::
    :toctree: generated/schema/
    :template: class.rst

    schema.CWUpload
    schema.UploadForm
    schema.UploadFile

:mod:`rql_download`: Associated hooks
-------------------------------------

.. autosummary::
    :toctree: generated/schema/
    :template: class.rst

    hooks.UploadHook
    hooks.ServerStartupHook
