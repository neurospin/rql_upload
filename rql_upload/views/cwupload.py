#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
import sys
import re
import copy
import traceback
from importlib import import_module
from packaging import version

# Cubicweb import
import cubicweb
cw_version = version.parse(cubicweb.__version__)
if cw_version >= version.parse("3.21.0"):
    from cubicweb import _

from cgi import parse_qs
from logilab.common.decorators import monkeypatch
from cubicweb import Binary
from cubicweb import ValidationError
from cubicweb.view import View
from cubicweb.web import Redirect
from cubicweb.web import formwidgets
from cubicweb.web import RequestError
from cubicweb.web.views.forms import FieldsForm
from cubicweb.web.views.formrenderers import FormRenderer
from cubicweb import Unauthorized
from cubicweb.predicates import authenticated_user

# RQL UPLOAD import
from .utils import load_forms
from .formfields import DECLARED_FIELDS


###############################################################################
# CWSearch Widgets
###############################################################################

class CWUploadForm(FieldsForm):
    """ Create a submit button.
    """
    __regid__ = "upload-form"
    title = _("Upload form")

    form_buttons = [formwidgets.SubmitButton(cwaction="apply")]


@monkeypatch(FormRenderer)
def render_content(self, w, form, values):
    """ Overwrite the original processing message when the upload is running.
    """
    if self.display_progress_div:
        w(u'<div id="progress" class="alert alert-warning">')
        w(u'<img width="50" src="{0}"/>'.format(
            self._cw.build_url('data/images/uploading.gif')))
        w(u'<b>Work in progress, please wait ...</b>')
        w(u'</div>')

    self.render_fields(w, form, values)
    self.render_buttons(w, form)


class CWUploadView(View):
    """ Custom view to edit the form generated from the instance
    configuration file [RQL_UPLOAD] -> upload_directory.

    If a synchrone check is defined in the 'SynchroneCheck' form 
    description, the check function will be executed. If an error is raised,
    a rollback is trigered. The check function has five inputs, a cnx, the
    posted data, and the upload, files and fields entities.

    Reserved keys are:

        * rql: a RQL that will be used to initialize another field.
          The associated field must contain a list.
          The field must be of the form <RQL>:<field_name>.
          It is possible to format the RQL string with the user login:
          use '{}' format synthax in your RQL to inherit from this
          functionality.

        * type: the field type that must be declared in the registry.

        * style: the css style that will be applied to the associated field
          div.

        * check_value: a regex used to chack the associated field.
    
        * required: point out manadatory fields.

    .. note::

        The authorized form fields are defined in the global parameter
        'DECLARED_FIELDS' that can be found in the
        'rql_upload.views.formfields.formfields' module.
    """
    __regid__ = "upload-view"
    title = _("Upload form")
    __select__ = authenticated_user()

    def call(self, **kwargs):
        """ Create the form fields.

        .. note::

            At upload, all field inputs are checked to match the 'check_value'
            regular expressions defined in the 'upload_structure_json' instance
            parameter.
        """
        # Get some parameters
        path = self._cw.relative_path()
        if "?" in path:
            path, param = path.split("?", 1)
            kwargs.update(parse_qs(param))
        form_name = kwargs["form_name"][0]
        code_in_study = kwargs.get("code_in_study", [None])[0]
        subject_eid = kwargs.get("subject_eid", [None])[0]

        # Get the form fields from configuration file
        config = load_forms(self._cw.vreg.config)

        # Create a structure to store values that must be checked before the
        # insertion in the data base
        check_struct = {}
        required_file_fields = {}

        # Update shortcut to access the uploaded files
        if 0:
            with self._cw.cnx._cnx.repo.internal_cnx() as cnx:
                rset = cnx.execute("Any X Where X is UploadFile")
                storage = cnx.repo.system_source._storages["UploadFile"]["data"]
                for index in range(rset.rowcount):
                    entity = rset.get_entity(index, 0)
                    eid = entity.eid
                    if eid not in self._cw.vreg.uploaded_file_names:
                        fpath = storage.current_fs_path(entity, "data")
                        self._cw.vreg.uploaded_file_names[eid] = fpath

        # If json file missing, generate error page
        if config == -1:
            self.w(u'<div class="panel panel-danger">')
            self.w(u'<div class="panel-heading">')
            self.w(u'<h2 class="panel-title">ERROR</h2>')
            self.w(u'</div>')
            self.w(u'<div class="panel-body">')
            self.w(u"<h3>Configuration file not found</h3>")
            self.w(u"Check that the path 'upload_structure_json' "
                    "declared in all-in-one.conf file is set.<br>")
            self.w(u"Then check that the path declared "
                    "(current path:'{0}') corresponds to a "
                    "json file and restart the instance.".format(
                        self._cw.vreg.config["upload_structure_json"]))
            self.w(u'</div>')
            self.w(u'</div>')
            return -1

        # If json can't be read, generate error page
        if config == -2:
            self.w(u'<div class="panel panel-danger">')
            self.w(u'<div class="panel-heading">')
            self.w(u'<h2 class="panel-title">ERROR</h2>')
            self.w(u'</div>')
            self.w(u'<div class="panel-body">')
            self.w(u"<h3>Configuration unknown</h3>")
            self.w(u"The json file configuring the form can't be "
                    "read: {0}".format(
                        self._cw.vreg.config["upload_structure_json"]))
            self.w(u'</div>')
            self.w(u'</div>')
            return -1

        # Create the form
        form = self._cw.vreg["forms"].select(
            "upload-form", self._cw, action="", form_name=form_name)
        fields_types = {}
        fields_labels = {}
        error_to_display = None
        try:
            # Go through each field description
            for field in config[form_name]["Fields"]:

                # Remove reserved field keys
                # > rql: a RQL that will be used to initialize another field.
                #   The current field must contain a list.
                #   Must be of the form <RQL>:<field_name>.
                #   Format the RQL string with the user login: use '{}' format
                #   synthax in your RQL to inherit from this functionality.
                if "rql" in field:
                    rql, dest_name = field.pop("rql").split(":")
                    rql = rql.format(self._cw.user.login)
                    if dest_name not in field:
                        raise ValueError(
                            "'{0}' not in field attributes.".format(dest_name))
                    if not isinstance(field[dest_name], list):
                        raise ValueError(
                            "'{0}' field attribute is not a list.".format(
                                dest_name))
                    rset = self._cw.execute(rql)
                    for row in rset.rows:
                        field[dest_name].extend(row)
                # > type: the field type that must be declared in the registry
                field_type = field.pop("type")
                fields_types[field["name"]] = field_type
                fields_labels[field["name"]] = field["label"]
                # > style: the css style that will be applied to the field div
                style = None
                if "style" in field:
                    style = field.pop("style")

                # Store the fields that must be checked using a Regex
                if "check_value" in field:
                    check_struct[field["name"]] = field.pop("check_value")

                # Check that the upload directory is created
                # If not display a danger message
                # Store also required file fields
                if field_type in ("FileField", "MultipleFileField"):
                    if not os.path.isdir(
                            self._cw.vreg.config["upload_directory"]):
                        self.w(u"<p class='label label-danger'>{0}: File "
                                "field can't be used because the "
                                "'upload_directory' has not been set in "
                                "all-in-ine.conf file or its path cannot be "
                                "created ({1})</p>".format(
                                    field.pop("label"),
                                    self._cw.vreg.config["upload_directory"]))
                        continue
                    if "required" in field and field["required"]:
                        required_file_fields[field["name"]] = field["label"]

                # If the field is in the registry add the field to the form
                # If requested add some custom styles to the field
                if field_type in DECLARED_FIELDS:
                    form.append_field(DECLARED_FIELDS[field_type](**field))
                    if style is not None:
                        widget = form.field_by_name(
                            field["name"]).get_widget(form)
                        widget.attrs["style"] = unicode(style)
                # Otherwise display a danger message
                else:
                    self.w(
                        u"<p class='label label-danger'>'{0}': Unknown field "
                         "type.</p>".format(field_type))

        # If something goes wrong during the form creation, display a danger
        # message and print the trace in the terminal
        except ValueError as error:
            print traceback.format_exc()
            error_to_display = error.message
        except:
            print traceback.format_exc()
            error_to_display = "The configuration file can't be read."

        # Display the error message
        if error_to_display is not None:
            self.w(u'<div class="panel panel-danger">')
            self.w(u'<div class="panel-heading">')
            self.w(u'<h2 class="panel-title">ERROR</h2>')
            self.w(u'</div>')
            self.w(u'<div class="panel-body">')
            self.w(u'<h3>Configuration file syntax error</h3>')
            self.w(u'{0}<br>'.format(error_to_display))
            self.w(u'Please refer to the documentation and make corrections')
            self.w(u'</div>')
            self.w(u'</div>')
            return -1

        # Form processings
        error_to_display = None
        try:
            # Retrieve the posted form field values
            posted = form.process_posted()

            # Check posted fields
            errors = self.check_posted(posted, required_file_fields,
                                       check_struct)
            if errors != {}:
                raise ValidationError(None, {})

            # Deal with subjects upload
            if form_name == "Subjects":

                # Create the study if necessary
                params = dict([(k, v)
                               if not isinstance(v, basestring)
                               else (k, unicode(v))
                               for k, v in posted.items()])
                if "study" not in params:
                    raise ValueError("Need a 'study' key in the 'Sujects' "
                                     "form definition.")
                study_name = params.pop("study")
                rset = self._cw.execute(
                    "Any ST Where ST is Study, ST name '{0}'".format(study_name))
                if rset.rowcount == 1:
                    study = rset.get_entity(0, 0)
                else:
                    study = self._cw.create_entity(
                        "Study",
                        name=unicode(study_name))

                # Add identifier attributes if not set
                if "identifier" not in params:
                    params[u"identifier"] = u"{0}_{1}".format(
                        study_name, params["code_in_study"])

                # Create the subject
                rset = self._cw.execute(
                    "Any S Where S is Subject, S code_in_study "
                    "'{0}'".format(params["code_in_study"]))
                if rset.rowcount == 1:
                    raise ValueError("Subject '{0}' already created.".format(
                        params["code_in_study"]))
                subject = self._cw.create_entity(
                    "Subject",
                    **params)
                created_entity = subject
                file_entities = None
                field_entities = None

                # Add relation between a subject and a study
                self._cw.execute(
                    "SET S study ST WHERE S eid '{0}', ST eid '{1}'".format(
                        subject.eid, study.eid))
                self._cw.execute(
                    "SET ST subjects S WHERE S eid '{0}', ST eid '{1}'".format(
                        subject.eid, study.eid))

            # Store upload in raw format
            else:

                # Create the CWUpload entity
                upload = self._cw.create_entity(
                    "CWUpload",
                    form_name=unicode(form_name),
                    status=u"Quarantine",
                    error=unicode(subject_eid))
                self._cw.execute(
                    "SET U error '' WHERE U eid '{0}'".format(upload.eid))
                created_entity = upload

                # Add subject relation if requested
                if code_in_study is not None:
                    self._cw.execute(
                        "SET S cwuploads U WHERE S eid '{0}', U eid "
                        "'{1}'".format(subject_eid, upload.eid))
                    self._cw.execute(
                        "SET U cwupload_subject S WHERE S eid '{0}', U eid "
                        "'{1}'".format(subject_eid, upload.eid))

                # Go through the posted form parameters. Deported fields are
                # stored in UploadFile entities, other fields in UploadField
                # entities
                file_eids = []
                field_eids = []
                file_entities = []
                field_entities = []
                for field_name, field_value in posted.items():

                    # > files are deported
                    if isinstance(field_value, Binary): 

                        # Create an UploadFile entity
                        extension = ".".join(field_value.filename.split(".")[1:])
                        entity = self._cw.create_entity(
                            "UploadFile",
                            name=field_name,
                            data=field_value,
                            data_extension=unicode(extension),
                            data_name=field_value.filename)
                        file_eids.append(entity.eid)
                        file_entities.append(entity)

                        # Add relation with the CWUpload entity
                        self._cw.execute("SET U upload_files F WHERE "
                                         "U eid %(u)s, F eid %(f)s",
                                         {"u": upload.eid, "f" : file_eids[-1]})

                    # > other fields are stored in the database
                    else:

                        # Create an UploadField entity
                        entity = self._cw.create_entity(
                            "UploadField",
                            name=unicode(field_name),
                            value=unicode(field_value),
                            type=unicode(fields_types[field_name]),
                            label=unicode(fields_labels[field_name]))
                        field_eids.append(entity.eid)
                        field_entities.append(entity)

                        # Add relation with the CWUpload entity
                        self._cw.execute("SET U upload_fields F WHERE "
                                         "U eid %(u)s, F eid %(f)s",
                                         {"u": upload.eid, "f" : field_eids[-1]})

            # Call synchrone check function
            check_func_desc = config[form_name].get("SynchroneCheck")
            if check_func_desc is not None:
                module_name = check_func_desc[:check_func_desc.rfind(".")]
                func_name = check_func_desc[check_func_desc.rfind(".") + 1:]
                module = import_module(module_name)
                check_func = getattr(module, func_name)
                try:
                    error_to_display = check_func(
                        self._cw.cnx, posted, created_entity, file_entities,
                        field_entities)
                except:
                    exc_type, exc_value, exc_tb = sys.exc_info()
                    raise Exception(traceback.format_exc())
                finally:
                    if error_to_display is not None:
                        raise ValidationError(
                            None, {None: "<br><br>" + error_to_display})

            # Redirection to the created CWUpload entity
            raise Redirect(self._cw.build_url(eid=created_entity.eid))

        # Handle exceptions
        except RequestError:
            pass
        except ValueError as error:
            error_to_display = error.message
        except ValidationError as error:
            # Check posted fields to concatenate the CW and application errors
            posted = {}
            for field in form.iter_modified_fields():
                posted[field.name] = form._cw.form[field.name]
            errors = self.check_posted(posted, required_file_fields,
                                       check_struct)
            concatenated_errors = {}
            for dict_struct in (errors, error.errors):
                for key, value in dict_struct.items():
                    concatenated_errors.setdefault(key, []).append(value)
            concatenated_errors = dict(
                (key, " - ".join(value))
                for key, value in concatenated_errors.items())
            raise ValidationError(None, concatenated_errors)
        except Redirect:
            raise
        except Unauthorized:
            error_to_display = "You are not allowed to upload data."
        except:
            print "RQL_UPLOAD: ", traceback.format_exc()
            error_to_display = ("Unexpected error, please contact the service "
                                "administrator.")
            raise ValidationError(
                None, {None: "<br><br>" + error_to_display})

        # Form rendering
        self.w(u"<legend>'{0}' upload form".format(form_name))
        if code_in_study is not None:
            self.w(u" for '{0}'".format(code_in_study))
        self.w(u"</legend>")     
        form.render(w=self.w, formvalues=self._cw.form)

        # Display the error message in the page
        if error_to_display is not None:
            self._cw.cnx.rollback()
            self.w(u'<div class="panel panel-danger">')
            self.w(u'<div class="panel-heading">')
            self.w(u'<h2 class="panel-title">ULPLOAD ERROR</h2>')
            self.w(u'</div>')
            self.w(u'<div class="panel-body">')
            self.w(u"{0}".format(error_to_display))
            self.w(u'</div>')
            self.w(u'</div>')

    def check_posted(self, posted, required_file_fields, check_struct):
        """ Check the posted values.

        Parameters
        ----------
        posted: dict
            the posted values.
        required_file_fields: dict
            the list of required file fields.
        check_struct: dict
            the fields to be checked using regexs.

        Returns
        -------
        errors: dict
            a dictionary with field names as keys and error as associated
            value.
        """
        # Output struct
        errors = {}

        # Check that required file fields are posted
        for required_field, field_label in required_file_fields.items():
            if required_field not in posted or posted[required_field] == "":
                errors[required_field] = "Value(s) required in field '{}'".format(
                    field_label)

        # Check value content
        for field_name, field_value in posted.items():
            # > check validity or not
            if field_name in check_struct:
                regex = check_struct[field_name]
                # > files 
                if isinstance(field_value, Binary):                   
                    value = self._cw.form[field_name][0]
                    message = (
                        "Find wrong file name '{0}' while searching "
                        "for extension '{1}'.".format(
                            value, regex))
                # > other fields
                else:
                    value = str(field_value)
                    message = (
                        "Find wrong parameter value '{0}' while "
                        "searching for pattern '{1}'.".format(
                            value, regex))
                # > check
                if re.match(regex, value) is None:
                    if field_name not in required_file_fields and value == "":
                        continue
                    if field_name in errors:
                        message = errors[field_name] + " - " + message
                    errors[field_name] = message                    

        return errors

