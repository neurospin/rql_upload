#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

from yams.buildobjs import EntityType, String, Bytes, RichString


class UploadFile(EntityType):
    """ An entity used to upload file which may contains binary data.
    """
    title = String(fulltextindexed=True, maxsize=256)
    data = Bytes(
        required=True, fulltextindexed=True,
        description=unicode("file to upload"))
    data_format = String(
        required=True, maxsize=128,
        description=unicode("MIME type of the file. Should be dynamically set "
                      "at upload time."))
    data_encoding = String(
        maxsize=32,
        description=unicode("encoding of the file when it applies (e.g. text). "
                            "Should be dynamically set at upload time."))
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
    data_path = String(required=True,
                  description=_("the path to the data that will be uploaded."))
    expiration_date = Date(required=True, indexed=True)
    data_type = String(required=True, default="", maxsize=50)

    # The link to the uploaded data
    has_data = SubjectRelation("UploadFile", cardinality="1*", inlined=True,
                             composite="subject")
    
