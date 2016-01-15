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
    global chk_server, disk_volume, lun_size, pool_option

    os.system('clear')
    print('[ Storage Adm ]\n[ Version {0} - © 2015 ]\n\n'.format(
        globalvar.version))

    stgadm = raw_input('STG Adm options\n\n'
                       '1. Add new volumes to existent host.\n'
                       '\nPlease choose an option: ')

    # Add new volumes to existent host menu

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
                lun_size = int(raw_input("Default LUN size (GB): "))
                break
            except (TypeError, ValueError):
                print(
                    '\tERROR: LUN Size need to be an int value.'
                    '\nDo not use GB. Example 100 for 100GB size of LUNs')

        if ':' in wwn_client:
            wwn_client = wwn_client.replace(':', '')

        # select storage
        get_stg = systemstorages.SystemStorages()
        get_stg.selectstorage()

        # get storage informations
        chk_server = emc_cmds.VMAX(config.symcli_path, get_stg.getsid(),
                                   wwn_client)

        print('\nCollecting some storage informations. Please wait...')

        ign = chk_server.get_ign()

        if ign[0] != 0:
            print('ERROR: {0}'.format(ign[1].replace('\n', '')))
            exit(1)
        else:
            ign = ign[1]

        mvn = chk_server.get_mvn(ign)

        if mvn[0] != 0:
            print('ERROR: {0}'.format(mvn[1]))
            exit(1)
        else:
            mvn = mvn[1]

        sgn = chk_server.get_sgn(mvn)

        if sgn[0] != 0:
            print('ERROR: {0}'.format(sgn[1]))
            exit(1)
        else:
            sgn = sgn[1]

        print('\nGetting information about pools from storage. Please wait...')

        # get storage pools
        lspool = chk_server.lspools()

        # check if command worked well.
        if lspool[0] != 0:
            print('Error: {0}'.format(lspool[1]))
            exit(1)

        lspool = lspool[1]
        print lspool
        lspool = lspool.split('\n')

        print('Select the Storage Pool from {0} storage (SID:{1})\n'
              .format(get_stg.getstorage(), get_stg.getsid()))

        # creating array to select storage pool
        pool_list = []

        for l_lspool in lspool[8:]:
            if l_lspool == '':
                break
            else:
                pool_list.append(l_lspool.split()[0])

        count = 0
        for l_pool in pool_list:
            print ('{0}: {1}'.format(count, l_pool))
            count += 1

        while True:
            try:
                pool_option = int(raw_input("Select the pool: "))
                break
            except IndexError:
                print(
                    '\tERROR: Select an existing option between'
                    '0 and {0}.'.format(count))

        print('\nConfig validation\n')
        print('\nClient Information')
        print(50 * '-')
        print('Register      : {0}'.format(change))
        print('Client Server : {0}'.format(hostname_client))
        print('Storage Name  : {0}'.format(storage_name))
        print('WWN Client    : {0}'.format(wwn_client))
        print('\nStorage Information')
        print(50 * '-')
        print('Storage Name          : {0}'.format(get_stg.getstorage()))
        print('Storage Type          : {0}'.format(get_stg.gettype()))
        print('Storage SID           : {0}'.format(get_stg.getsid()))
        print('Initiator Group Name  : {0}'.format(ign))
        print('Making View Names     : {0}'.format(mvn))
        print('Storage Group Name    : {0}'.format(sgn))
        print('Storage Pool          : {0}'.format(pool_list[pool_option]))
        print('\nInformations about the request:')
        print(50 * '-')
        print('Disk Volume   : {0}'.format(disk_volume))
        print('LUN Size      : {0}'.format(lun_size))
        print('')
