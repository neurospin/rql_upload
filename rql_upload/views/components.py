#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CW import
from cubicweb.predicates import nonempty_rset, anonymous_user
from cubicweb.web import component

# RQL UPLOAD import
from utils import load_forms


###############################################################################
# CW upload box
###############################################################################

class CWUploadBox(component.CtxComponent):
    """ Class that generate a left box on the web browser to access all the
    decalred forms in the 'upload_structure_json' cubicweb instance parameter.

    It will appear on the left and contain the names if all forms defined in the
    json file.
    
    If a 'Subjects' name is defined, organize the collect using the subjects
    as pivotal entities.

    .. warning::

        It will NOT appear for anonymous users.
    """
    __regid__ = "ctx-upload-box"
    __select__ = (component.CtxComponent.__select__ & ~anonymous_user())
    title = _("Upload forms")
    context = "left"
    order = 0

    def render_body(self, w, **kwargs):
        """ Method that creates the upload navigation box (generates html code).

            This method displays error messages if the forms can't be extracted
            from the configuration file.
        """
        # Get the field form structure
        forms = self._cw.vreg.forms
        if forms == -1:
            href = self._cw.build_url("view", vid="upload-view",
                                      title=self._cw._("Upload form"),
                                      form_name='ERROR: no json found')
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u'{0}</a>'.format("ERROR: no json found."))
            w(u'</div></div>')
            return

        elif forms == -2:
            href = self._cw.build_url("view", vid="upload-view",
                                      title=self._cw._("Upload form"),
                                      form_name="ERROR: json file can't be read")
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group-vertical btn-block">')
            w(u'<a class="btn btn-primary" href="{0}">'.format(href))
            w(u"{0}</a>".format("ERROR: at least one json file can't be read."))
            w(u'</div></div>')
            return

        # Organize the collect using subjects as pivotal entities
        if self._cw.vreg.subjects_mapping is not None:
            self._create_btn_new_form(w, "Subjects", title="Add new subject")
            self._subject_search_box(w)

        # List all forms
        else:
            # Create a link to each form declared in the settings
            for form_name in forms:
                self._create_btn_new_form(w, form_name)

        # Create a button to access my upload
        w(u'<hr>')
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(
            rql=("Any U ORDERBY U DESC Where U is CWUpload"
                 ", U created_by X, X login '{}'".format(self._cw.user.login))
        )
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'<span class="glyphicon glyphicon glyphicon-cloud-upload">'
            '</span> My uploads</a>')
        w(u'</div></div><br/>')

        # Create a button to access all authorized upload
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        href = self._cw.build_url(
            rql="Any U ORDERBY U DESC Where U is CWUpload")
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'<span class="glyphicon glyphicon glyphicon-cloud-upload">'
            '</span> All uploads</a>')
        w(u'</div></div><br/>')

        # Create a button to access the uploads summary board
        rset = self._cw.execute("Any N Where S is Study, S name N")
        study_names = [line[0] for line in rset.rows]
        if len(study_names) > 0:
            w(u'<hr>')

            # > main button
            w(u'<div class="btn-toolbar">')
            w(u'<div class="btn-group btn-group-justified">')
            w(u'<a class="btn btn-info"'
               'data-toggle="collapse" data-target="#summary-boards" '
               'style="width:100%">')
            w(u'Summary boards</a>')
            w(u'</div></div>')
            # > typed buttons container
            w(u'<div id="summary-boards" class="collapse">')
            w(u'<div class="panel-body">')
            w(u'<hr>')
            # > typed buttons
            for name in study_names:
                href = self._cw.build_url("view", vid="summary-uploads-board",
                                           study=name)
                w(u'<div class="btn-toolbar">')
                w(u'<div class="btn-group btn-group-justified">')
                w(u'<a class="btn btn-primary" href="{0}" style="width:100%">'.format(href))
                w(u'{0}</a>'.format(name))
                w(u'</div></div><br/>')
            w(u'<hr>')
            w(u'</div></div><br/>')

    def _create_btn_new_form(self, w, form_name, title=None):
        """ Create a new button to fill a new form.
        """
        href = self._cw.build_url("view", vid="upload-view",
                                  title=self._cw._("Upload form"),
                                  form_name=form_name)
        w(u'<div class="btn-toolbar">')
        w(u'<div class="btn-group-vertical btn-block">')
        w(u'<a class="btn btn-primary" href="{0}">'.format(href))
        w(u'<span class="glyphicon glyphicon glyphicon-list">'
            '</span>')
        w(u' {0}</a>'.format(title or form_name))
        w(u'</div></div><br/>')

    def _subject_search_box(self, w):
        """ Create a search box for subjects.
        """
        # JS
        basesearch = "view?rql=Any+X+Where+X+is+Subject%2C+X+code_in_study+"
        w(u'<script>')
        w(u'function SubjectSearchBox() {')
        w(u'var link = "{0}" + "\'" + '
           'document.getElementById("link-box").value + "\'";'.format(basesearch))
        w(u'window.location = link;')
        w(u'}')
        w(u'</script>')

        # Add search box
        w(u'<div class="btn-toolbar">')
        w(u'<input type="text" id="link-box">')
        w(u'<input type="button" id="link" value="Search" '
           'onClick="SubjectSearchBox()">')
        w(u'</div>')

