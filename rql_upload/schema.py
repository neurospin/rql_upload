#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from yams.buildobjs import EntityType, String, Bytes, RichString, SubjectRelation   
from cubicweb.schema import ERQLExpression, RQLUniqueConstraint


class UploadFile(EntityType):
    """ An entity used to upload file which may contains binary data.

    Attributes
    ----------
    title: String (optional)
        a short description of the file.
    data: Bytes (mandatory)
        contains the uploaded file.
    data_extension: String (mandatory)
        the uploaded file extension.
    data_name: String (mandatory)
        the uploaded file name.
    data_sha1hex: String (optional)
        SHA1 sum of the file.
    """
    title = String(fulltextindexed=True, maxsize=256)
    data = Bytes(
        required=True, fulltextindexed=True,
        description=unicode("file to upload"))
    data_extension = String(
        required=True, maxsize=32,
        description=unicode("the upload file extension."))
    data_name = String(
        required=True, fulltextindexed=True,
        description=unicode("name of the file. Should be dynamically set at "
                            "upload time."))
    data_sha1hex = String(
        maxsize=40,
        description=unicode("SHA1 sum of the file. May be set at upload time."),
        __permissions__={"read": ("managers", "users", "guests"),
                         "add": (),
                         "update": ()})
    description = RichString(fulltextindexed=True, internationalizable=True,
                             default_format="text/rest")


class CWUpload(EntityType):
    """ An entity used to to store a form.

    Attributes
    ----------
    title: String (mandatory)
        the name of the upload (has to be unique in the data base).
    form_name: String (mandatory)
        the name of the form we upload.
    result_data: SubjectRelation (optional)
        the link(s) to the uploaded file.
    result_form: SubjectRelation (mandatory)
        the link to the form.
    """
    # Set default permissions
    __permissions__ = {
        "read":   ("managers", ERQLExpression("X owned_by U"),),
        "add":    ("managers", "users"),
        "delete": ("managers", "owners"),
        "update": ("managers", "owners"),
    }
    # Entity parameters
    title = String(
        maxsize=256, required=True,
        constraints=[
            RQLUniqueConstraint(
                "X title N, S title N, X owned_by U, X is CWUpload",
                mainvars="X",
                msg=_("this name is already used"))
        ])
    form_name = String(maxsize=256, required=True)

    # The link to the uploaded data
    result_data = SubjectRelation(
        "UploadFile", cardinality="**", composite="subject")
    result_form = SubjectRelation(
        "File", cardinality="**", composite="subject")
    
