#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


options = (
    (
        "upload_directory",
        {
            "type": "string",
            "default": "",
            "help": "base directory in which the files are uploaded.",
            "group": "rql_upload", "level": 0,
        }
    ),
    (
        "upload_structure_json",
        {
            "type": "csv",
            "default": "",
            "help": ("json files describing the different upload entities. "
                     "If a 'subjects' file is specified organize the upload "
                     "by subject."),
            "group": "rql_upload", "level": 0,
        }
    ),
    (
        "upload_log_dir",
        {
            "type": "string",
            "default": "",
            "help": "base directory in which log file is written.",
            "group": "rql_upload", "level": 0,
        }
    ),
    (
        "validated_directory",
        {
            "type": "string",
            "default": "",
            "help": "base directory in which the validated files are deported.",
            "group": "rql_upload", "level": 0,
        }
    ),
    (
        "default_asynchrone_delay",
        {
            "type": "float",
            "default": 30,
            "help": "specifies the asynchrone looping check delay (in minutes).",
            "group": "rql_upload", "level": 0,
        }
    ),
)
