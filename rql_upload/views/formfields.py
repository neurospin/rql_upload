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

from cubicweb.web import formfields


# Define global parameter
DECLARED_FIELDS = {}

###############################################################################
# Registration callback
###############################################################################


def registration_callback(vreg):
    """ The authorized form fields are registered from this function.

    The registration identifier must be of the form '<class_name>'.
    The preregistered fields are:

    * **Basic fields**: StringField - PasswordField - IntField -
      FloatField - BooleanField - DateField - DateTimeField - TimeField -
      TimeIntervalField.

    * **Compound fields**: FileField.
    """

    # Got through fields we want to register
    for field_name in ["StringField", "PasswordField",
                       "IntField", "FloatField", "BooleanField",
                       "DateField", "DateTimeField",
                       "TimeField", "TimeIntervalField", "FileField"]:

        # Define class parameters
        DECLARED_FIELDS[field_name] = formfields.__dict__[field_name]
