#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import os
import globalvar
import systemstorages
import config
import emc_cmds


def main_menu():
    os.system('clear')
    print('[ Storage Adm ]\n[ Version {0} - © 2015 ]\n\n'.format(
        globalvar.version))

    stgadm = raw_input('STG Adm options\n\n'
                       '1. Add new volumes to existent host.\n'
                       '\nPlease choose an option: ')

    if stgadm == '1':

        print('\n\nRequest informations:\n')
        change = raw_input('Ticket/Change/Work Order: ')
        hostname_client = raw_input('Hostname Client: ')
        storage_name = raw_input('Storage Name: ')
        wwn_client = raw_input('WWN Client: ').lower()

        if ':' in wwn_client:
            wwn_client = wwn_client.replace(':', '')

        get_stg = systemstorages.SystemStorages()
        get_stg.selectstorage()

        print('\nConfig validation:\n')
        print('Registar      : {0}'.format(change))
        print('Client Server : {0}'.format(hostname_client))
        print('Storage Name  : {0}'.format(storage_name))
        print('WWN Client    : {0}'.format(wwn_client))
        print('Storage Name  : {0}'.format(get_stg.getstorage()))
        print('Storage Type  : {0}'.format(get_stg.gettype()))
        print('Storage SID   : {0}'.format(get_stg.getsid()))

        print('\nChecking the configurations of server...')

        chk_server = emc_cmds.VMAX(config.symcli_path, get_stg.getsid(),
                                   wwn_client)

        if config.modeop == 'demo':
            # test using data_tests
            chk_server = emc_cmds.VMAX(config.stghome + '/stgadm/data_tests/',
                                       get_stg.getsid(), wwn_client)

            ign = chk_server.init_ign_test()

        else:

            ign = chk_server.init_ign()

        if 'The specified initiator was not found' in ign:
            print('Sorry, {0}'.format(ign))
            exit(1)

        print ('Getting the Initiator Group Name: {0}'.format(ign))

        mgv = chk_server.init_mvn(ign)

        print('Getting the Making View Names: {0}'.format(mgv))

        ign = chk_server.init_sgn(mgv)

        print('Getting the Storage Group Name: {0}'.format(ign))
