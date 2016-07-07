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
from cubes.piws.views.primary import PIWSPrimaryView
from cubicweb.predicates import is_instance


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
        self.w(u"<table class='table cw-table-primary-entity'>")
        self.render_attribute("&nbsp", upload.symbol, table=True)
        self.w(u"</table>")

        # Display the upload fields
        labels = ["Label", "Value"]
        index = 0
        for fields, title, label1, label2 in [
                (upload.upload_fields, "Fields", "label", "value"),
                (upload.upload_files, "Files", "data_name", "data_sha1hex")]:
            if len(fields) > 0:
                records = []
                for field in fields:
                    records.append([field.name,
                                    getattr(field, label1),
                                    getattr(field, label2)])
                self.wview("jtable-hugetable-clientside", None, "null",
                           labels=labels, records=records, csv_export=True,
                           title=title, elts_to_sort="ID", use_scroller=True,
                           index=index)
                index += 1


def registration_callback(vreg):
    """ Register the tuned primary views.
    """
    vreg.register(CWUploadPrimaryView)
