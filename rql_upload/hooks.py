#! /usr/bin/env python
##########################################################################
# NSAp - Copyright (C) CEA, 2013
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


# System import
import os

# CW import
from cubicweb.server import hook


class ServerStartupHook(hook.Hook):
    """ At the server startup, initialize the upload rules.

    An UploadFile entity data is deported on the server file system.
    To do so, we configure the UploadFile 'data' attribute with the
    BytesFileSystemStorage storage.
    """
    __regid__ = "rql_upload.serverstartup"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        """ Configuring the BytesFileSystem storage.
        """
        # In order sphinx to work properly: cw modify the path
        from cubicweb.server.sources import storages

        # Get the defined upload folder
        upload_dir = self.repo.vreg.config["upload_directory"]

        # Create the folder if necessary
        if not os.path.exists(upload_dir):
            os.makedirs(upload_dir)

        # Configure the storage folder
        storage = storages.BytesFileSystemStorage(upload_dir)

        # Configure the storage file content
        storages.set_attribute_storage(self.repo, "UploadFile", "data", storage)
