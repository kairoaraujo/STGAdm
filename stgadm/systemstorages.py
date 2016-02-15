#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import config


class SystemStorages:
    """ Select, List and Show Systems Storages from config file. """

    def __init__(self, stg_sys='', stg_type='', stg_sig=''):

        self.stg_sys = stg_sys
        self.stg_type = stg_type
        self.stg_sid = stg_sig

    pass

    def selectstorage(self):
        """ Selection in ASCII mode Systems Storage. """

        global storage_option
        print ("\n[Storage Selection]\n"
               "\nSelect the system storage used by client:")
        storages_keys = list(config.storages.keys())
        storages_length = (len(config.storages.keys())) - 1
        count = 0
        while count <= storages_length:
            print ("{0} : {1}".format(count, storages_keys[count]))
            count += 1

        while True:
            try:
                storage_option = int(raw_input("System Storage: "))
                self.stg_sys = (storages_keys[storage_option])
                break
            except (IndexError, ValueError):
                print(
                    '\tERROR: Select an existing option between'
                    '0 and {0}.'.format(storages_length))

        self.stg_type = config.storages[('{0}'.format(storages_keys
                                                      [storage_option]))][0]
        self.stg_sid = config.storages[('{0}'.format(storages_keys
                                                     [storage_option]))][1]

    def getstorage(self):

        return self.stg_sys

    def gettype(self):

        return self.stg_type

    def getsid(self):

        return self.stg_sid
