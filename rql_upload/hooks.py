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
from importlib import import_module
import json

# CW import
from cubicweb import ValidationError
from cubicweb.server import hook
from cubicweb.predicates import is_instance

# Package import
from cubes.rql_upload.views.utils import load_forms
from cubes.rql_upload.views.utils import get_cwuploads


class CWUploadSubjectHook(hook.Hook):
    """ When using the subject collection type, assess that only one valid
    upload can be found for each form of the study the subject is concerned by.
    """
    __regid__ = "rql_upload.upload-subject-unicity"
    __select__ = hook.Hook.__select__ & is_instance("CWUpload")
    events = ("after_add_entity", )
    order = -1  # should be run before other hooks

    def __call__(self):
        """ If a valid upload is found with the same associated form name,
        do not create again this upload: unicity constrain.
        """
        # This hook is activated only if the subject collection strategy is
        # used
        if self._cw.vreg.subjects_mapping is not None:

            # Get all the uploads related with this subject
            subject_eid = self.entity.cw_edited["error"]
            rset = self._cw.execute("Any X Where X eid '{0}'".format(
                subject_eid))
            subject_entity = rset.get_entity(0, 0)
            cwuploads = get_cwuploads(subject_entity)

            # Based on the latest upload status reject this creation or not
            latest_upload_desc = cwuploads.get(
                self.entity.form_name, [None])[-1]
            if latest_upload_desc is None:
                return
            latest_status = latest_upload_desc[0].lower()

            if latest_status in ("validated", "quarantine", "canceled"):
                raise ValidationError(
                    "CWUpload", {
                        "unicity not respected": _(
                            "Subject '{0}' already have a '{1}' upload with "
                            "status '{2}'. Please wait or contact the system "
                            "administrator.".format(
                                subject_entity.code_in_study,
                                self.entity.form_name,
                                latest_status))})


class UploadFileHook(hook.Hook):
    """ An upload file entity is created/updated,
    store a fingerprint of binary data fields.
    """
    __regid__ = "rql_upload.upload"
    __select__ = hook.Hook.__select__ & is_instance("UploadFile")
    events = ("before_add_entity", "before_update_entity")
    order = -1  # should be run before other hooks

    def __call__(self):
        """ If a 'data' field is uploaded, compute the associated fingerprint.
        """
        if "data" in self.entity.cw_edited:
            self.entity.set_format_and_encoding()
            data = self.entity.cw_edited["data"]
            if data is not None:
                data = self.entity.compute_sha1hex(data.getvalue())
            self.entity.cw_edited["data_sha1hex"] = data


class ServerStartupHook(hook.Hook):
    """ Deport files on file system rather than database indexation.

    An 'UploadFile' entity data is deported on the server file system.
    To do so, we configure the 'UploadFile' 'data' attribute with the
    'BytesFileSystemStorage' storage.
    The repository location is defined at the instance creation
    'upload_directory' (instance parameter).
    If no instance parameter is set, the 'file' field won't be created.

    Execute asynchrone checks defined defined in the configuration file
    section [RQL UPLOAD] -> upload_structure_json -> AsynchroneCheck.

    Define a shortcut to access the uploaded files 'uploaded_file_names'. It
    maps an 'UploadFile' eid to the uploded resource location on the server
    file system.

    Store the upload type in the 'upload_type' configuration parameter.
    """
    __regid__ = "rql_upload.serverstartup"
    events = ("server_startup", "server_maintenance")

    def __call__(self):
        """ Configuring the 'BytesFileSystem' storage.
        """
        # In order sphinx to work properly: cw modify the path
        from cubicweb.server.sources import storages

        # Get the defined upload folder
        upload_dir = self.repo.vreg.config["upload_directory"]

        # Get the defined validated folder
        validated_dir = self.repo.vreg.config["validated_directory"]

        # Create the folder if necessary
        try:
            if not os.path.exists(upload_dir):
                os.makedirs(upload_dir)
            if not os.path.exists(validated_dir):
                os.makedirs(validated_dir)

            # Configure the storage folder
            storage = storages.BytesFileSystemStorage(upload_dir)

            # Configure the storage file content
            storages.set_attribute_storage(self.repo, "UploadFile", "data",
                                           storage)
        except:
            pass

        # Execute all asynchrone check defined in [RQL UPLOAD] ->
        # upload_structure_json -> AsynchroneCheck in the CW task loop
        forms = load_forms(self.repo.vreg.config)
        self.repo.vreg.forms = forms
        self.repo.vreg.subjects_mapping = None
        delay_in_sec = self.repo.vreg.config["default_asynchrone_delay"] * 60.
        if isinstance(forms, dict):
            if "Subjects" in forms:
                self.repo.vreg.subjects_mapping = forms["Subjects"].pop(
                    "Mapping")
            for form_name in forms:
                check_func_desc = forms[form_name].get("ASynchroneCheck")
                if check_func_desc is not None:
                    module_name = check_func_desc[:check_func_desc.rfind(".")]
                    func_name = check_func_desc[check_func_desc.rfind(".") + 1:]
                    module = import_module(module_name)
                    check_func = getattr(module, func_name)
                    self.repo.looping_task(delay_in_sec, check_func, self.repo)

        # Shortcut to access the uploaded files
        self.repo.vreg.uploaded_file_names = {}
