# coding: utf-8
##########################################################################
# NSAp - Copyright (C) CEA, 2017
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import os
from packaging import version

# Cubicweb import
import cubicweb
cw_version = version.parse(cubicweb.__version__)
if cw_version >= version.parse("3.21.0"):
    from cubicweb import _

from cubicweb.view import View
from logilab.common.registry import yes
from cubicweb.predicates import authenticated_user

# Package import
from cubes.rql_upload.views.utils import get_cwuploads


class SummaryUploadBoard(View):
    """
    """
    __regid__ = "summary-uploads-board"
    __select__ = authenticated_user()
    title = _("Uploads summary board")

    def call(self):
        """ Get all the uploads of one study.
        """
        # Get the view parameters
        study = self._cw.form["study"]

        # Get the subjects
        rql = "Any S Where S is Subject, S study ST, ST name '{0}'".format(
            study)
        rset = self._cw.execute(rql)

        # Build the table header
        headers = self._cw.vreg.subjects_mapping[study]

        # Build the record
        records = []
        pending_url = self._cw.data_url(
            os.path.join("images", "yellow_dot.png"))
        image_template = u"<img alt='' src='{0}'>"
        for subject_entity in rset.entities():
            record = ([subject_entity.code_in_study] +
                      [image_template.format(pending_url)] * len(headers))
            for form_name, uploads in get_cwuploads(subject_entity).items():
                index = headers.index(form_name) + 1
                status = uploads[-1][0].lower()
                status_url = self._cw.data_url(uploads[-1][2].symbol)
                record[index] = image_template.format(status_url)
            records.append(record)

        # Call JhugetableView for html generation of the table
        self.wview("jtable-hugetable-clientside", None, "null", labels=headers,
                   records=records, csv_export=False, title=self.title,
                   timepoint="", elts_to_sort=["ID"],
                   use_scroller=False, tooltip_name=None)
