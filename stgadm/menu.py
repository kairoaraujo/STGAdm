#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import os
import globalvar
import systemstorages
import config
import fields
import emc_cmds


def main_menu():
    os.system('clear')
    print('[ Storage Adm ]\n[ Version {0} - © 2015 ]\n\n'.format(
        globalvar.version))

    stgadm = raw_input('STG Adm options\n\n'
                       '1. Add new volumes to existent host.\n'
                       '\nPlease choose an option: ')

    if stgadm == '1':

        print('\n\nRequest informations\n')
        change = fields.Fields('change', 'Ticket/Change/Work Order: ')
        change.chkfieldstr()
        change = change.strvarout()

        hostname_client = fields.Fields('hostname', 'Hostname Client: ')
        hostname_client.chkfieldstr()
        hostname_client = hostname_client.strvarout()

        storage_name = raw_input('Storage Name: ')

        wwn_client = fields.Fields('wwn_client', 'WWN Server Client: ')
        wwn_client.chkfieldstr()
        wwn_client = wwn_client.strvarout()

        disk_volume = int()
        lun_size = int()

        while True:
            try:
                disk_volume = int(raw_input("Total Disk Required (GB): "))
                break
            except (TypeError, ValueError):
                print(
                    '\tERROR: Total Disk need to be an int value in GB. '
                    '\nDo not use GB. Example: 1000 for 1000GB (1TB)')

        while True:
            try:
                lun_size = int(raw_input("Default size for disks: "))
                break
            except (TypeError, ValueError):
                print(
                    '\tERROR: LUN Size need to be an int value.'
                    '\nDo not use GB. Example 100 for 100GB size of LUNs')

        if ':' in wwn_client:
            wwn_client = wwn_client.replace(':', '')

        get_stg = systemstorages.SystemStorages()
        get_stg.selectstorage()

        print('\nConfig validation\n')
        print('\nClient Information')
        print(50 * '-')
        print('Register      : {0}'.format(change))
        print('Client Server : {0}'.format(hostname_client))
        print('Storage Name  : {0}'.format(storage_name))
        print('WWN Client    : {0}'.format(wwn_client))
        print('\nStorage Information')
        print(50 * '-')
        print('Storage Name  : {0}'.format(get_stg.getstorage()))
        print('Storage Type  : {0}'.format(get_stg.gettype()))
        print('Storage SID   : {0}'.format(get_stg.getsid()))

        print('\nChecking the configurations of server on Storage ...')

        chk_server = emc_cmds.VMAX(config.symcli_path, get_stg.getsid(),
                                   wwn_client)

        ign = chk_server.init_ign()

        if 'The specified initiator was not found' in ign:
            print('Sorry, {0}'.format(ign))
            exit(1)

        print ('Initiator Group Name : {0}'.format(ign))

        mgv = chk_server.init_mvn(ign)

        print('Making View Names     : {0}'.format(mgv))

        ign = chk_server.init_sgn(mgv)

        print('Storage Group Name    : {0}'.format(ign))

        print('\nInformations about the request:')
        print(50 * '-')
        print('Disk Volume   : {0}'.format(disk_volume))
        print('LUN Size      : {0}'.format(lun_size))
