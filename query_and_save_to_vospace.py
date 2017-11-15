#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from time import sleep
from threading import Thread
from xml.dom.minidom import parseString

from eas.eas_qry import EAS_Query
from vos.vos_push import VOSpace_Push

import urllib.parse as urlparse
import urllib.request as urlrequest
import requests, ssl, base64, json
import sys


def exec_query(adql, folder, file_name, user, pwd):
    easHdl = EAS_Query()
    easHdl.setQuery(adqlQry=adql)

    if not easHdl.run():
        print("ERROR while executing the query:\n{}".format(adql))
        sys.exit(1)

    #print(easHdl.results())
    vos = VOSpace_Push()
    if not vos.save_to_file(folder=folder, file=file_name,
                            data=easHdl.results(),
                            user=user, pwd=pwd):
        print("ERROR while storing query results in VOSpace")
        sys.exit(2)

    print("File '{}' with query results stored in your VOSpace folder {}".format(file_name, folder))


def main():

    exec_query(adql="SELECT DISTANCE(POINT('ICRS', rightascension, declination), " +
                                    "POINT('ICRS',16.41683,4.90781)) AS dist, " +
                           "* FROM sc3_mer_cat_10 " +
                    "WHERE 1=CONTAINS(POINT('ICRS', rightascension, declination), " +
                                     "CIRCLE('ICRS',16.41683,4.90781, 26)) " +
                    "ORDER BY dist ASC", 
               folder='queries', file_name='my_query_results.csv', 
               user='myuser', pwd='mypasswd')


if __name__ == '__main__':
    main()