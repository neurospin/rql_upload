#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.web.views import baseviews
from cubicweb.predicates import is_instance


class FileUploadOutOfContext(baseviews.OutOfContextView):
    """ Display a nice out of context view with a small icon on the left.
    """
    __select__ = is_instance("UploadFile")

    def cell_call(self, row, col):
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<img src="{0}" alt="{1}"/>'.format(
            entity.icon_url(),
            self._cw._("icon for {0}").format(entity.data_extension)))
        super(FileUploadOutOfContext, self).cell_call(row, col)
