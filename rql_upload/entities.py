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
from cubicweb.entities import AnyEntity


class EntityUploadFile(AnyEntity):
    """ Define the 'UploadFile' entity associated functions.
    """
    __regid__ = "UploadFile"

    def dc_title(self):
        """ Method the defined the upload file entity title.
        """
        return self.data_name

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        #config = self._cw.vreg.config
        return self._cw.data_url(os.path.join("icons", "upload.ico"))


class EntityUploadForm(AnyEntity):
    """ Define the 'UploadFile' entity associated functions.
    """
    __regid__ = "UploadForm"

    def dc_title(self):
        """ Method the defined the upload file entity title.
        """
        return self.data_name

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        #config = self._cw.vreg.config
        return self._cw.data_url(os.path.join("icons", "upload.ico"))
