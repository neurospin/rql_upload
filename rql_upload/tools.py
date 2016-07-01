#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################

import logging


def get_or_create_logger(config):
    logger = logging.getLogger("rql_upload")
    if len(logger.handlers) > 0:
        return logger

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter(
        ('%(asctime)s --%(levelname)s-- %(message)s'
         ' [%(module)s.%(funcName)s (%(lineno)d)]'))
    handler = logging.StreamHandler()
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    path = config["upload_log_dir"]
    if path:
        path += '/rql_upload.log'
        handler = logging.FileHandler(path)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
    return logger
