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
from yams.buildobjs import SubjectRelation
from cubicweb.schema import ERQLExpression
from cubicweb.schema import RRQLExpression

# Brainomics import
from cubes.brainomics2.schema.medicalexp import Subject


###############################################################################
# Modification of the schema
###############################################################################

UPLOAD_PERMISSIONS = {
    "read": (
        "managers",
        ERQLExpression("X created_by U")),
    "add": ("managers", ),
    "update": ("managers", ),
    "delete": ("managers", ),
}

UPLOAD_RELATION_PERMISSIONS = {
    "read": (
        "managers",
        "users"),
    "add": (
        "managers",
        RRQLExpression("S in_assessment A, U in_group G, G can_update A")),
    "delete": (
        "managers",
        RRQLExpression("S in_assessment A, U in_group G, G can_update A"))
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

    # The name field used in the form
    name = String(
        maxsize=64,
        required=True,
        description=unicode("name field used in form"))
    # The value defined in the form
    value = RichString(
        default_format="text/rest",
        description=unicode("the value defined in the form."))
    # The value type
    type = String(
        maxsize=256,
        required=True,
        description=unicode("the value type."))
    # The label used in the form
    label = String(
        maxsize=64,
        required=True,
        description=unicode("the label used in the form."))


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

    # The name of the form used to upload data
    form_name = String(
        maxsize=256,
        required=True,
        description=unicode("form name label used to upload data."))
    # The status of the upload
    status = String(
        required=True,
        vocabulary=("Quarantine", "Rejected", "Validated", "Canceled"),
        description=unicode("upload status."))
    # The error message of the upload
    error = RichString(
        default_format="text/rest",
        description=unicode("eror message."))


class upload_files(RelationDefinition):
    """ Define the relation between CWUpload and UploadFile
    A CWUpload has 0..n UploadFile.
    An UploadFile has 1 CWUpload.
    """
    __permissions__ = UPLOAD_RELATION_PERMISSIONS

    inlined = False
    subject = "CWUpload"
    object = "UploadFile"
    cardinality = "*1"
    composite = "subject"


class upload_fields(RelationDefinition):
    """ Define the relation between CWUpload and UploadField
    A CWUpload has 0..n UploadField.
    An UploadField has 1 CWUpload.
    """
    __permissions__ = UPLOAD_RELATION_PERMISSIONS

    inlined = False
    subject = "CWUpload"
    object = "UploadField"
    cardinality = "*1"
    composite = "subject"


class cwuploads(RelationDefinition):
    """ Define the relation between Subject and CWUpload
    A Subject has 0..n CWUpload.
    A CWUpload has 0..1 Subject.
    """
    __permissions__ = UPLOAD_RELATION_PERMISSIONS

    inlined = False
    subject = "Subject"
    object = "CWUpload"
    cardinality = "*?"


class cwupload_subject(RelationDefinition):
    """ Define the relation between CWUpload and Subject
    A CWUpload has 0..1 Subject.
    A Subject has 0..n CWUpload.
    """
    __permissions__ = UPLOAD_RELATION_PERMISSIONS

    inlined = False
    subject = "CWUpload"
    object = "Subject"
    cardinality = "?*"
