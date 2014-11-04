#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import json
import os

# CW import
from cgi import parse_qs
from logilab.mtconverter import xml_escape
from cubicweb import Binary
from cubicweb.web.views.forms import FieldsForm
from cubicweb.view import View
from cubicweb.web import formfields
from cubicweb.web import formwidgets
from cubicweb.web import RequestError, ProcessFormError

# RQL UPLOAD import
from utils import load_forms


###############################################################################
# CWSearch Widgets
###############################################################################

class CWUploadForm(FieldsForm):
    """ Allowed fields

    Basic fields
    ------------

    .. autoclass:: cubicweb.web.formfields.StringField()
    .. autoclass:: cubicweb.web.formfields.PasswordField()
    .. autoclass:: cubicweb.web.formfields.IntField()
    .. autoclass:: cubicweb.web.formfields.BigIntField()
    .. autoclass:: cubicweb.web.formfields.FloatField()
    .. autoclass:: cubicweb.web.formfields.BooleanField()
    .. autoclass:: cubicweb.web.formfields.DateField()
    .. autoclass:: cubicweb.web.formfields.DateTimeField()
    .. autoclass:: cubicweb.web.formfields.TimeField()
    .. autoclass:: cubicweb.web.formfields.TimeIntervalField()

    Compound fields
    ---------------

    .. autoclass:: cubicweb.web.formfields.RichTextField()
    .. autoclass:: cubicweb.web.formfields.FileField()
    .. autoclass:: cubicweb.web.formfields.CompoundField()
    """
    __regid__ = "upload-form"

    form_buttons = [formwidgets.SubmitButton(cwaction="apply")]
    upload_title = formfields.StringField(
        name="upload_title", label="Title", required=True, value="<unique>")


class CWUploadView(View):
    """ Custom widget to edit the form from the configuration file.
    """
    __regid__ = "upload-view"

    bool_map = {
        "True": True,
        "False": False
    }

    def call(self, **kwargs):
        """ Create the 'form' fields.
        """
        # Get some parameters
        path = self._cw.relative_path()
        if "?" in path:
            path, param = path.split("?", 1)
            kwargs.update(parse_qs(param))
        form_name = kwargs["form_name"][0]

        # Get the form fields
        config = load_forms(self._cw.vreg.config)

        # Create the form       
        form = self._cw.vreg["forms"].select(
            "upload-form", self._cw, action="", form_name=form_name)
        for field in config[form_name]:
            field_type = field.pop("type")
            if field_type == "BooleanField" and "value" in field:
                field["value"] = self.bool_map[field["value"]]
            if "required" in field:
                field["required"] = self.bool_map[field["required"]]
            form.append_field(formfields.__dict__[field_type](**field))

        # Form processings
        try:
            posted = form.process_posted()

            # Get the form parameters
            inline_params = {}
            deported_params = {}
            for field_name, field_value in posted.iteritems():
                if isinstance(field_value, Binary):
                    deported_params[field_name] = field_value
                else:
                    inline_params[field_name] = field_value

            # Save the inline parameters in a File entity
            form_eid = self._cw.create_entity(
                "File", data=Binary(json.dumps(inline_params)),
                data_format=u"text/json", data_name=u"form.json").eid

            # Save deported parameters in UploadFile entities
            upload_file_eids = []
            for field_name, field_value in deported_params.iteritems():
                print form.field_by_name(field_name).format_field
                print form.field_by_name(field_name).encoding_field
                upload_file_eids.append(self._cw.create_entity(
                    "UploadFile", data=field_value, data_format=u"",
                    data_name=unicode(inline_params["upload_title"])).eid)

            # Create the CWUpload entity
            self._cw.create_entity(
                "CWUpload", title=unicode(inline_params["upload_title"]),
                form_name=unicode(form_name), result_form=form_eid,
                result_data=upload_file_eids).eid
            
            self.w(u'<p>posted values %s</p>' % xml_escape(repr(posted)))
        except RequestError:
            pass

        # Form rendering
        self.w(u'<h3 class="panel-title">Upload ("{0}" form)</h3>'.format(form_name))
        form.render(w=self.w, formvalues=self._cw.form)

