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
import json
import collections

# CW import
from cubes.piws.views.primary import PIWSPrimaryView
from cubicweb.predicates import is_instance

# Package import
from cubes.rql_upload.views.utils import get_cwuploads


class CWUploadPrimaryView(PIWSPrimaryView):
    """ Class that define how to display an CWUpload entity.
    """
    __select__ = PIWSPrimaryView.__select__ & is_instance("CWUpload")
    title = _("Upload form")

    def render_entity_attributes(self, upload):
        """ Generate the html code.
        """
        # Inherit page style
        super(PIWSPrimaryView, self).render_entity_attributes(upload)

        # Display a header
        #self.w(u"<table class='table cw-table-primary-entity'>")
        #self.render_attribute("&nbsp", upload.symbol, table=True)
        #self.w(u"</table>")

        # Display the upload fields
        labels = ["Value"]
        index = 0
        for fields, title, label1, label2 in [
                (upload.upload_fields, "Fields", "label", "value"),
                (upload.upload_files, "Files", "data_name", "data_sha1hex")]:
            if len(fields) > 0:
                records = []
                for field in fields:
                    records.append([getattr(field, label1),
                                    getattr(field, label2)])
                self.wview("jtable-hugetable-clientside", None, "null",
                           labels=labels, records=records, csv_export=True,
                           title=title, elts_to_sort="ID", use_scroller=True,
                           index=index)
                index += 1


class SubjectPrimaryView(PIWSPrimaryView):
    """ Class that define how to display a Subject entity.
    """
    __select__ = PIWSPrimaryView.__select__ & is_instance("Subject")

    def render_entity_attributes(self, entity):
        """ Generate the html code.
        """
        # Inherit page style
        super(PIWSPrimaryView, self).render_entity_attributes(entity)

        # Deal with subjects data collection style
        if self._cw.vreg.subjects_mapping is not None:

            # Check which forms are concerned by this subject based on
            # the study-forms mapping
            study_name = entity.study[0].name
            if study_name not in self._cw.vreg.subjects_mapping:
                return
            concerned_forms = self._cw.vreg.subjects_mapping[study_name]
            
            # Create a link to each form
            cwuploads = get_cwuploads(entity)
            from pprint import pprint
            for index, form_name in enumerate(concerned_forms):
                self._display_pending_form(
                    form_name, entity.code_in_study, entity.eid,
                    cwuploads.get(form_name, [None]), index)

    def _display_pending_form(self, form_name, code_in_study, subject_eid,
                              cwuploads, index):
        """ Create a new button to fill a new form.
        """
        # Get the pending symbole
        last_upload = cwuploads[-1]
        if last_upload is not None:
            symbol = last_upload[2].symbol
            created_by = last_upload[2].created_by[0].login
            status = last_upload[0].lower()
            info = "({0}-{1})".format(created_by,
                                    last_upload[1].strftime("%Y/%m/%d"))
        else:
            symbol = os.path.join("images", "yellow_dot.png")
            status = "pending"
            info = ""
        image = u"<img alt='' src='{0}'>".format(self._cw.data_url(symbol))

        # Create form url
        href = self._cw.build_url(
            "view", vid="upload-view", title=self._cw._("Upload form"),
            code_in_study=code_in_study, form_name=form_name,
            subject_eid=subject_eid)

        # Create the div that will contain the list item
        self.w(u"<div class='form-ooview'><div class='well'>")

        # Create a bootstrap row item
        self.w(u"<div class='row'>")
        # > first element: the image
        self.w(u"<div class='col-md-4'><p style='margin-top:8px'>"
                "{0} <strong>{1} {2}</strong></p></div>".format(
                    image, status, info))
        # > second element: the entity description + link
        self.w(u"<div class='col-md-4'><h4>{0}</h4>".format(form_name))
        self.w(u"</div>")
        # > third element: the create button if necessary
        self.w(u"<div class='col-md-4'>")
        self.w(u"<div class='secondary-buttons'>")
        if status in ("pending", "rejected"):
            self.w(u"<a href='{0}' target=_blank class='btn btn-success' "
                   "type='button' style='margin-right:8px'>".format(href))
            self.w(u"Submit &#9735;")
            self.w(u"</a>")
        # > fourth element: the see more button with the history
        self.w(u"<button class='btn btn-danger' type='button' "
               "style='margin-right:8px' data-toggle='collapse' "
               "data-target='#history-{0}'>".format(index))
        self.w(u"History")
        self.w(u"</button>")

        self.w(u"</div>")
        self.w(u"</div>")
        
        # Close divs
        self.w(u"</div>")

        # Get the entity related history
        history_desc = collections.OrderedDict()
        for upload_desc in cwuploads[:-1]:
            created_by = upload_desc[2].created_by[0].login
            key = "{0}-{1}".format(created_by,
                                   upload_desc[1].strftime("%Y/%m/%d %H:%M:%s"))
            error = upload_desc[2].error or ""
            error = error.replace("<", "&lt;")
            history_desc[key] = "{0} <pre>{1}</pre>".format(
                upload_desc[0].lower(), error)
        if len(history_desc) == 0:
            history_desc[""] = "No history available."

        # Create a div that will be show or hide when the history button is
        # clicked
        self.w(u"<div id='history-{0}' class='collapse'>".format(index))
        self.w(u"<dl class='dl-horizontal'>")
        for key, value in history_desc.items():
            self.w(u"<dt>{0}</dt><dd>{1}</dd>".format(key, value))
        self.w(u"</div>")

        # Close divs
        self.w(u"</div></div>")


def registration_callback(vreg):
    """ Register the tuned primary views.
    """
    vreg.register(CWUploadPrimaryView)
    vreg.register(SubjectPrimaryView)
