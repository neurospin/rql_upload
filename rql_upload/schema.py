##########################################################################
# NSAp - Copyright (C) CEA, 2013 - 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# CubicWeb import
from yams.buildobjs import EntityType
from yams.buildobjs import String
from yams.buildobjs import Bytes
from yams.buildobjs import RichString
from yams.buildobjs import RelationDefinition
from cubicweb.schema import ERQLExpression


###############################################################################
# Modification of the schema
###############################################################################

UPLOAD_PERMISSIONS = {
    "read": (
        "managers", "uploaders"),
        #ERQLExpression("X created_by U")),
    "add": ("managers", "uploaders"),
    "update": ("managers", ),
    "delete": ("managers", ),
}

RELATION_PERMISSIONS = {
    "read": (
        "managers",
        "users"),
    "add": ("managers",),
    "delete": ("managers",),
}


class UploadFile(EntityType):
    """ An entity used to upload file which may contain binary data.

    Attributes
    ----------
    name: String (mandatory)
        name field used in form.
    data: Bytes (mandatory)
        contains the uploaded file.
    data_extension: String (mandatory)
        the uploaded file extension.
    data_name: String (mandatory)
        the uploaded file name.
    data_sha1hex: String (optional)
        SHA1 sum of the file.
    """

    # Set default permissions
    __permissions__ = UPLOAD_PERMISSIONS

    name = String(
        maxsize=64,
        required=True,
        description=unicode("name field used in form"))
    data = Bytes(
        required=True,
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
        description=unicode("SHA1 sum of the file. May be set at upload time.")
    )


class UploadField(EntityType):
    """ An entity used to upload data but not file.

    Attributes
    ----------
    name: String (mandatory)
        the name field used in the form.
    value: String
        the value defined in the orm.
    type: String (mandatory)
        the value type.
    label: String (mandatory)
        the label used in the form.
    """

    # Set default permissions
    __permissions__ = UPLOAD_PERMISSIONS

    # the name field used in the form
    name = String(
        maxsize=64,
        required=True,
        description=unicode("name field used in form"))
    # the value defined in the form
    value = RichString(
        default_format="text/rest",
        description=unicode("value defined in form"))
    # the value type
    type = String(
        maxsize=256,
        required=True,
        description=unicode("value type"))
    # the label used in the form
    label = String(
        maxsize=64,
        required=True,
        description=unicode("label used in form"))


class CWUpload(EntityType):
    """ An entity used to upload data.

    Attributes
    ----------
    form_name: String (mandatory)
        the name of the form used to upload data.
    status: String (mandatory)
        the status od the upload.
        the value must be 'Quarantine', 'Rejected' or 'Validated'.
    error: String
        the message error if the stutis is 'Rejected'
    """

    # Set default permissions
    __permissions__ = UPLOAD_PERMISSIONS

    # the name of the form used to upload data
    form_name = String(
        maxsize=256,
        required=True,
        description=unicode("form name label used to upload data"))
    # the status of the upload
    status = String(
        required=True,
        vocabulary=('Quarantine', 'Rejected', 'Validated'),
        description=unicode("upload status"))
    # the eror message of the upload
    error = RichString(
        default_format="text/rest",
        description=unicode("eror message"))


class upload_files(RelationDefinition):
    """ Define the relation between CWUpload and UploadFile
    A CWUpload have 0..n UploadFile.
    An UploadFile have 1 CWUpload.
    """

    __permissions__ = RELATION_PERMISSIONS
    inlined = False
    subject = "CWUpload"
    object = "UploadFile"
    cardinality = "*1"
    composite = "subject"


class upload_fields(RelationDefinition):
    """ Define the relation between CWUpload and UploadField
    A CWUpload have 0..n UploadField.
    An UploadField have 1 CWUpload.
    """

    __permissions__ = RELATION_PERMISSIONS
    inlined = False
    subject = "CWUpload"
    object = "UploadField"
    cardinality = "*1"
    composite = "subject"
