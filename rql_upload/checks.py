##########################################################################
# NSAp - Copyright (C) CEA, 2016
# Distributed under the terms of the CeCILL-B license, as published by
# the CEA-CNRS-INRIA. Refer to the LICENSE file or to
# http://www.cecill.info/licences/Licence_CeCILL-B_V1-en.html
# for details.
##########################################################################


def demo_example1_synchrone(posted, cnx):
    """ Dummy: check that the integer times float result is equal to two.
    This function raise an exception if the float value is equal to two.
    """
    if posted["float"] == 2:
        raise ValueError("The float value must be different than two.")
    result = posted["integer"] * posted["float"]
    error_message = None
    if result != 2:
        error_message = "The integer times float result must be equal to two."
    return error_message


def demo_example1_asynchrone(repo):
    """ Dummy: check that the string field is equal to 'a'.
    """
    with repo.internal_cnx() as cnx:
        rset = cnx.execute("Any X, V Where X is CWUpload, X form_name "
                           "'Example1', X status 'Quarantine', X "
                           "upload_fields F, F name 'string', F value V")
    for eid, string_value in rset:
         if string_value == "a":
            status = "Validated"
         else:
            status = "Rejected"
         with repo.internal_cnx() as cnx:
            cnx.execute("SET X status '{0}' WHERE X eid '{1}'".format(
                status, eid))
            cnx.commit()

