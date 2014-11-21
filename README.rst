==========
RQL UPLOAD
==========


Summary
=======

Cube to upload data in a cubicweb CWUpload entity.


How to
======

When creating a cubicweb instance that derived from the 'rql_download' cube,
two parameters need to be specified:

* **upload_directory**: the directory where the file will be uploaded.
* **upload_structure_json**: the file that contains the forms descriptions.

When starting the instance, after the logging, a left 'Upload' box appear. This
box contains a link to all the forms defined in the 'upload_structure_json'
file. Note that the form settings in the 'upload_structure_json' file can be
updated dynamically.


Defining the forms
==================

Write a '*.json' file that need to be set in the 'all-in-one.conf'
'upload_structure_json' parameter. The authorized form fields are defined
in the 'cubicweb.web.formfields' module:

* Basic fields: StringField - PasswordField - IntField - BigIntField -
  FloatField - BooleanField - DateField - DateTimeField - TimeField - 
  TimeIntervalField.

* Compound fields: RichTextField - FileField.

Each field is described with a dictionary with keys:

* name (mandatory): the name of the field (ie., an identifier).
* label (mandatory): the name of the field that will be visible from the
  web browser.
* type (mandatory): the field type (one of basic fields or compound fields).
* required (optional, default False): specify that the field has to be filled.
* value (optional): the default field value.
* check_value (optional): a regular expression pattern that will be used to
  check if the field is properly filled.

An example with three forms 'test1', 'test2' and 'test3':

.. code-block:: python

    {
        "test1": [
            {
                "name": "string", "type": "StringField",
                "value": "", "label": "string"},
            {
                "name": "dropdown", "type": "StringField",
                "value": "", "label": "dropdown",
                "choices": ["choice_1", "choice_2"]},
            {
                "name": "integer", "type": "IntField",
                "required": "True", "value": 2,"label": "integer"},
            {
                "name": "float", "type": "FloatField",
                "required": "True", "value": 1.2, "label": "float"},
            {
                "name": "boolean", "type": "BooleanField",
                "required": "True", "value": "True", "label": "boolean"},
            {
                "name": "date", "type": "DateField",
                "required": "False", "label": "date"}
        ],

        "test2": [
            {
                "name": "string", "type": "StringField",
                "required": "True", "value": "", "label": "string"},
            {
                "name": "file", "type": "FileField",
                "required": "False", "label": "file"}
        ],

        "test3": [
            {
                "name": "file1", "type": "FileField",
                "required": "False", "label": "file1", "check_value": ".*zip"},
            {
                "name": "file2", "type": "FileField",
                "required": "False", "label": "file2"}
        ]
    }


    






