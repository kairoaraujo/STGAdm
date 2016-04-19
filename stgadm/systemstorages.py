#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

import config


class SystemStorages(object):
    """Select, List and Show Systems Storages from config file. """

    def __init__(self, stg_sys=None, stg_type=None, stg_sid=None,
                 vnx_1ip=None, vnx_2ip=None, vnx_user=None, vnx_pass=None,
                 vnx_scope=None):
        self.stg_sys = stg_sys
        self.stg_type = stg_type
        self.stg_sid = stg_sid
        self.vnx_1ip = vnx_1ip
        self.vnx_2ip = vnx_2ip
        self.vnx_user = vnx_user
        self.vnx_pass = vnx_pass
        self.vnx_scope = vnx_scope

    def selectstorage(self):
        """Selection in ASCII mode Systems Storage. """

        global storage_option
        print("\n[Storage Selection]\n"
              "\nSelect the system storage used by client:")
        storages_keys = list(sorted(config.storages.keys()))
        storages_length = (len(config.storages.keys())) - 1
        count = 0
        while count <= storages_length:
            print("{0} : {1}".format(count, storages_keys[count]))
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

        if self.stg_type == 'EMC_VNX':
            self.vnx_1ip = self.stg_sid
            self.vnx_2ip = config.storages[('{0}'.format(
                storages_keys[storage_option]))][2]
            self.vnx_user = config.storages[('{0}'.format(
                storages_keys[storage_option]))][3]
            self.vnx_pass = config.storages[('{0}'.format(
                storages_keys[storage_option]))][4]
            self.vnx_scope = config.storages[('{0}'.format(
                storages_keys[storage_option]))][5]

    def getstorage(self):

        return self.stg_sys

    def gettype(self):

        return self.stg_type

    def getsid(self):

        return self.stg_sid

    def getvnx_1ip(self):

        return self.vnx_1ip

    def getvnx_2ip(self):

        return self.vnx_2ip

    def getvnx_user(self):

        return self.vnx_user

    def getvnx_pass(self):

        return self.vnx_pass

    def getvnx_scope(self):

        return self.vnx_scope
