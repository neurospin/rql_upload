#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from cubicweb.predicates import nonempty_rset, anonymous_user
from cubicweb.web import component


###############################################################################
# CW upload box
###############################################################################

class CWUploadBox(component.CtxComponent):
    __regid__ = "ctx-upload-box"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    context = "left"
    order = 0

    def render(self, w, **kwargs):
        url  = self._cw.build_url("add/CWUpload")
        w(u'<div class="well">')
        w(u'<h4>{0}</h4>'.format(self._cw._("Upload")))
        w(u'<a class="btn btn-primary btn-block" id="{0}" href="{1}">'.format(
            'upload-link', url))
        w(u'<span class="glyphicon glyphicon-save"> {0}</span>'.format(
            self._cw._("Upload")))
        w(u'</a>')
        w(u'</div>')

