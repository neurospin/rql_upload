:orphan:

.. _views_guide:

###################
Views documentation
###################

Documentation regarding views defined on the cube.

.. currentmodule:: rql_upload.views

.. _views_nav:

:mod:`rql_upload.views`: Navigation
===================================

All the views designed to navigate on the web pages. The 'CWUploadBox' resume
all the forms available. A 'UploadOutOfContext' out of context view is also
proposed to render the 'UploadFile' and 'UploadForm' summary views.

User Views
----------

.. autosummary::
    :toctree: generated/navigation/
    :template: class.rst

    components.CWUploadBox
    outofcontext.UploadOutOfContext

Associated Tools
----------------

.. autosummary::
    :toctree: generated/navigation/
    :template: function.rst

    utils.load_forms
    formfields.registration_callback


.. _views_form:

:mod:`rql_upload.views.cwupload`: Form
======================================

A view 'CWUploadView' that displays the form to fill.

User Views
----------

.. autosummary::
    :toctree: generated/form/
    :template: class.rst

    cwupload.CWUploadView

Associated Tools
----------------

.. autosummary::
    :toctree: generated/form/
    :template: class.rst

    cwupload.CWUploadForm

.. autosummary::
    :toctree: generated/form/
    :template: function.rst

    cwupload.render_content
