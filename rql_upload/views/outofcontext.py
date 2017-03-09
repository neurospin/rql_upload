#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
from packaging import version

# Cubicweb import
import cubicweb
cw_version = version.parse(cubicweb.__version__)
if cw_version >= version.parse("3.21.0"):
    from cubicweb import _

from cubicweb.web.views import baseviews
from cubicweb.predicates import is_instance


class UploadOutOfContext(baseviews.OutOfContextView):
    """ Display a nice out of context view with a small icon on the left of
    uploded items.
    """
    __select__ = is_instance("UploadFile", "UploadForm")

    def cell_call(self, row, col):
        """ Create the html code.
        """
        entity = self.cw_rset.get_entity(row, col)
        self.w(u'<img src="{0}" alt="{1}"/>'.format(
            entity.icon_url(), self._cw._("'upload' icon")))
        super(UploadOutOfContext, self).cell_call(row, col)
