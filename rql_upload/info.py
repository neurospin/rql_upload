#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

""" This file contains the module information.
"""

_version_major = 0
_version_minor = 0
_version_micro = 1

# Format expected by setup.py and doc/source/conf.py: string of form "X.Y.Z"
__version__ = "{0}.{1}.{2}".format(
    _version_major, _version_minor, _version_micro)

CLASSIFIERS = ["Development Status :: 3 - Alpha",
               "Environment :: Console",
               "Operating System :: OS Independent",
               "Programming Language :: Python",
               "Topic :: Scientific/Engineering",
               "Topic :: Utilities"]

description = "Rql Upload"

long_description = """
==========
Rql Upload
==========

Cube to upload data in a cubicweb CWUpload entity.
"""

# versions for dependencies
SPHINX_MIN_VERSION = 1.0

# Main setup parameters
NAME = "rql_upload"
MAINTAINER = "Antoine Grigis"
MAINTAINER_EMAIL = "antoine.grigis@cea.fr"
DESCRIPTION = description
LONG_DESCRIPTION = long_description
URL = "https://github.com/neurospin/rql_upload"
DOWNLOAD_URL = "https://github.com/neurospin/rql_upload"
LICENSE = "CeCILL-B"
CLASSIFIERS = CLASSIFIERS
AUTHOR = "NSAp developers"
AUTHOR_EMAIL = "antoine.grigis@cea.fr"
PLATFORMS = "OS Independent"
MAJOR = _version_major
MINOR = _version_minor
MICRO = _version_micro
VERSION = __version__
PROVIDES = ["rql_upload"]
REQUIRES = []
EXTRA_REQUIRES = {"doc": ["sphinx>=1.0"]}
