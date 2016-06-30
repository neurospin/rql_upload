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

# CW import
from cubicweb.web.views.primary import PrimaryView
from cubicweb.predicates import is_instance
from logilab.mtconverter import xml_escape


class UploadFormPrimaryView(PrimaryView):
    """ Class that define how to display an UploadForm entity.

    The table display may be tuned by specifing the 'upload-table' class in
    a css.
    """
    __select__ = PrimaryView.__select__ & is_instance("UploadForm")
    title = _("Upload form")

    def display_form(self, entity):
        """ Generate the html code.
        """
        # Get the json form
        json_data = json.load(entity.data)

        # Get the associated CWUpload entity
        # cwupload = entity.reverse_result_form[0]

        # Display a title
        self.w(u'<div class="page-header">')
        self.w(u'<h2>{0}</h2>'.format(xml_escape(entity.dc_title())))
        self.w(u'</div>')

        self.w(u'<table class="upload-table">')

        # Display the form
        for label, attribute in json_data.iteritems():
            self.w(u'<tr><td><b>{0}</b></td><td>{1}</td></tr>'.format(
                   self._cw._(label), attribute))

        # Link to the upload entity
        # self.w(u'<tr><td><b>{0}</b></td><td>{1}</td></tr>'.format(
        #        self._cw._("Related upload"), cwupload.view("outofcontext")))

        self.w(u'</table>')

    def call(self, rset=None):
        """ Create the form primary view.
        """
        # Get the entity that contains the form
        entity = self.cw_rset.get_entity(0, 0)

        # Display the form
        self.display_form(entity)


class CWUploadView(PrimaryView):
    """
    """

    __select__ = PrimaryView.__select__ & is_instance("CWUpload")

    def call(self, rset=None):
        eUpload = self.cw_rset.get_entity(0, 0)
        self.w(u'<div class="page-header">')
        self.w(u'<h2>')
        if eUpload.status == 'Quarantine':
            self.w(u"<span class='glyphicon glyphicon-cog' />")
        elif eUpload.status == 'Rejected':
            self.w(u"<span class='glyphicon glyphicon-remove' />")
        elif eUpload.status == 'Validated':
            self.w(u"<span class='glyphicon glyphicon-ok' />")
        else:
            self.w(u"<span class='glyphicon glyphicon-cloud-upload' />")
        self.w(u' {}</h2>'.format(eUpload.dc_title()))
        self.w(u'</div>')

        self.w(u'<div>')
        self.w(u'<h3>Status</h3>')
        self.w(u'<b>{}</b>'.format(eUpload.status))
        print 'error: {}'.format(eUpload.error)
        if eUpload.error:
            self.w(u'<div class="panel panel-danger">{}</div>'.format(
                eUpload.error))
        self.w(u'</div>')

        self.w(u'<div>')
        self.w(u'<h3>Fields</h3>')
        self.w(u'<table class="upload-table">')
        self.w(u'<tr><th>Name</th><th>Value</th></tr>')
        for eField in sorted(eUpload.upload_fields,
                             key=lambda field:field.name):
            self.w(u'<tr><td>{0}</td><td>{1}</td></tr>'.format(
                   eField.label, eField.value))
        self.w(u'</table>')
        self.w(u'</div>')

        self.w(u'<div>')
        self.w(u'<h3>Files</h3>')
        self.w(u'<table class="upload-table">')
        self.w(u'<tr><th>Name</th><th>SHA1</th></tr>')
        for eFile in eUpload.upload_files:
            self.w(u'<tr><td>{0}</td><td>{1}</td></tr>'.format(
                   eFile.data_name, eFile.data_sha1hex))
        self.w(u'</table>')
        self.w(u'</div>')


def registration_callback(vreg):
    """ Register the tuned primary views.
    """
    vreg.register(UploadFormPrimaryView)
    vreg.register(CWUploadView)
