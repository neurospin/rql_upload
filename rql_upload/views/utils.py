#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

# System import
import json
import os
from bisect import bisect_left


def load_forms(cw_config):
    """ Function to load the forms structures from the file defined in the
    'upload_structure_json' cubicweb instance parameter.

    Parameters
    ----------
    cw_config: dict
        the cubicweb configuration built from the instance 'all-in-one.conf'
        file.

    Returns
    -------
    config: dict
        the forms descriptions defined in the 'upload_structure_json' setting
        files.
    -1
        if a configuration file is not specified or found on the system.
    -2
        if a configuration file cannot be decoded as json file.
    """
    # Go through each configuration file
    config_files = cw_config["upload_structure_json"]
    config = {}
    for path in config_files:

        # Try to load the json file
        if not os.path.isfile(path):
            return -1
        try:
            with open(path) as open_json:
                config.update(json.load(open_json))
        except:
            return -2
    return config


def get_cwuploads(subject_entity):
    """ Sort the subject uploads.

    Create a dictionary with form name as keys associated with a
    sorted list by dates of 3-uplets (status, date, entity).
    """
    cwuploads = {}
    for upload_entity in subject_entity.cwuploads:
        status = upload_entity.status
        date = upload_entity.creation_date
        if upload_entity.form_name not in cwuploads:
            cwuploads[upload_entity.form_name] = [
                (status, date, upload_entity)]
        else:
            keys = [elem[1] for elem in cwuploads[upload_entity.form_name]]
            index = bisect_left(keys, date)
            cwuploads[upload_entity.form_name].insert(
                index, (status, date, upload_entity))
    return cwuploads
