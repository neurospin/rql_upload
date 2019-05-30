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
import hashlib

# CW import
from cubicweb.entities import AnyEntity


class EntityUploadField(AnyEntity):
    """ Define the 'UploadField' entity associated functions. """

    __regid__ = "UploadField"
    __bootstap_glyph__ = True

    def dc_title(self):
        """ Method that defines the upload field entity title. """

        return self.label

    @property
    def symbol(self):
        return "<span class='glyphicon glyphicon-edit'></span>"


class EntityUploadFile(AnyEntity):
    """ Define the 'UploadFile' entity associated functions.
    """
    __regid__ = "UploadFile"
    __bootstap_glyph__ = True

    def set_format_and_encoding(self):
        """ Try to set format and encoding according to known values (filename,
        file content, format, encoding).

        This method must be called in a before_[add|update]_entity hook else it
        won't have any effect.
        """
        return

    def compute_sha1hex(self, value=None):
        """ Compute a hash of the data.
        """
        if value is None and self.data is not None:
            value = self.data.getvalue()
        if value is not None:
            return unicode(hashlib.sha1(value).hexdigest())

    def dc_title(self):
        """ Method that defines the upload file entity title.
        """
        return self.data_name

    def icon_url(self):
        """ Method to get an icon for this entity.
        """
        return self._cw.data_url(os.path.join("icons", "upload.ico"))

    @property
    def symbol(self):
        return "<span class='glyphicon glyphicon-file'></span>"

    def get_file_path(self):
        """ Return the file path of the UploadFile using a sql query.
        """
        sql = "SELECT cw_data FROM cw_uploadfile WHERE cw_eid = '{0}'"
        sql = sql.format(self.eid)
        if hasattr(self._cw, "system_sql"):
            cursor = self._cw.system_sql(sql)
        else:
            cursor = self._cw.cnx.system_sql(sql)
        path = cursor.fetchall()[0][0].__str__()
        return path


class EntityCWUpload(AnyEntity):
    """ Define the 'CWUpload' entity associated functions. """

    __regid__ = "CWUpload"
    __bootstap_glyph__ = False

    def dc_title(self):
        """ Method that defines the upload entity title.
        """
        return u"{} by {} on {} at {}".format(
            self.form_name,
            self.dc_creator(),
            self.creation_date.strftime('%Y-%m-%d'),
            self.creation_date.strftime('%H:%M:%S')
        )

    @property
    def symbol(self):
        if self.status == "Quarantine":
            return os.path.join("images", "orange_dot.png")
        elif self.status in ("Rejected", "Canceled"):
            return os.path.join("images", "red_dot.png")
        elif self.status == "Validated":
            return os.path.join("images", "green_dot.png")
        else:
            return os.path.join("images", "yellow_dot.png")

    def get_field_value(self, field_name):
        """ Return the value of the UploadField with the field_name.
            Return None if the upload not have the related UploadField.
        """
        for eField in self.upload_fields:
            if eField.name == field_name:
                return eField.value
        return None
