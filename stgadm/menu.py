#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import os
import globalvar
import systemstorages
import config
import fields
import pystorage
import vmax_add_dev
import ds8k_add_dev
import findchange
import getid


def menu_emc_vmax(change=None, hostname_client=None, storage_name=None,
                  stg_name=None, stg_type=None, stg_sid=None, wwn_client=None):
    # get storage informations
    global pool_option, mvn_option

    if not os.path.isdir(config.symcli_path):
        print ("\nERROR: SYMCLI path dir not found. Check config file item "
               "symcli_path.")
        exit()

    chk_server = pystorage.EMC.VMAX(config.symcli_path)

    print('\nCollecting some storage informations. Please wait...')

    ign = chk_server.get_ign(stg_sid, wwn_client)

    if ign[0] != 0:
        print('ERROR: {0}'.format(ign[1].replace('\n', '')))
        exit(1)

    else:
        ign = ign[1]

    mvn = chk_server.get_mvn(stg_sid, ign)

    if mvn[0] != 0:
        print('ERROR: {0}'.format(mvn[1]))
        exit(1)

    else:

        print('\nInitiator Group Name from \033[1;32m{0}\033[1;00m identified '
              'as \033[1;32m{1}\033[1;00m.'.format(wwn_client, ign))
        print('Mask View Name(s) on storage is '
              '\033[1;32m{0}\033[1;00m'.format(mvn[1:]))

        if len(mvn) > 2:
            count = 0
            mvn.remove(mvn[0])

            print('\nMultiples MVN detected. Please choose an MVN.\n')
            for l_mvn in mvn:
                print ('{0}: {1}'.format(count, l_mvn))
                count += 1

            while True:
                try:
                    mvn_option = int(raw_input("Select the MVN: "))
                    break
                except (IndexError, ValueError):
                    print('\tERROR: Select an existing option between'
                          '0 and {0}.'.format(count))

            mvn = mvn[mvn_option]

        else:
            mvn = mvn[1]

    sgn = chk_server.get_sgn(stg_sid, mvn)

    if sgn[0] != 0:
        print('ERROR: {0}'.format(sgn[1]))
        exit(1)
    else:
        sgn = sgn[1]

    print('Storage Group Name on storage is '
          '\033[1;32m{0}\033[1;00m'.format(sgn))

    print('\nGetting information about pools from storage. Please wait...')

    # get storage pools
    lspool = chk_server.lspools(stg_sid, config.lspool_args)

    # check if command worked well.
    if lspool[0] != 0:
        print('Error: {0}'.format(lspool[1]))
        exit(1)

    print('\n[POOL Selection]')
    lspool = lspool[1]
    print lspool
    lspool = lspool.split('\n')

    print('Select the Storage Pool from \033[1;32m{0}\033[1;00m storage'
          ' (SID: \033[1;32m{1}\033[1;00m)\n'
          .format(stg_name, stg_sid))

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
        except (IndexError, ValueError):
            print(
                '\tERROR: Select an existing option between'
                '0 and {0}.'.format(count))

    def choose_device_type():
        print('Select the type of device you want create:\n')
        print('0. Meta device')
        print('1. Regular device')
        device_type = raw_input('\nChoose an option: ')

        if device_type == '0':

            device_type = 'meta'

            while True:
                try:
                    size_check = 1

                    while size_check != 0:
                        member_size = int(raw_input(
                            'What is the size of member? (GB): '))
                        size_check = lun_size % member_size
                        if size_check != 0:
                            print('ERRO: The member size ({0} GB) needs to '
                                  'be an integer divisor by the '
                                  'LUN Size ({1}GB).'
                                  .format(member_size, lun_size))

                        else:
                            return member_size, device_type

                    break
                except (TypeError, ValueError):
                    print(
                        '\tERROR: Total Disk need to be an int value in GB.'
                        '\nDo not use GB. Example: 1000 for 1000GB (1TB)')

        elif device_type == '1':

            device_type = 'regular'
            member_size = 0
            return member_size, device_type

        else:
            print('ERRO: Wrong option.')
            choose_device_type()

    device_config = choose_device_type()
    member_meta_size = device_config[0]
    lun_type = device_config[1]

    disk_count = disk_volume / lun_size

    new_change = vmax_add_dev.New(change, hostname_client, storage_name,
                                  wwn_client, stg_name, stg_type, stg_sid,
                                  ign, mvn, sgn, pool_list[pool_option],
                                  disk_volume, lun_size, lun_type,
                                  member_meta_size, disk_count)

    new_change.preview()

    save_config = fields.YesNo('Do you would like save this allocation?[y/n]: ',
                               'n')
    save_config = save_config.check()

    if save_config == 'y':

        new_change.headerchange()
        new_change.writechange()
        end_change = new_change.closechange()
        print end_change

    else:
        print('Finishing. Thank you.')


def menu_ibm_ds8k(change=None, hostname_client=None, storage_name=None,
                  stg_name=None, stg_type=None, stg_sid=None, wwn_client=None):
    global pool_1_option, pool_2_option, code_1_pool, code_2_pool

    if not os.path.isfile(config.dscli_bin):
        print ("\nERROR: DSCLI not found. Check config file item dscli_bin.")
        exit()

    if not os.path.isfile(config.dscli_profile_path + '/' + stg_sid):
        print ("\nERROR: DSCLI not found. Check config file item "
               "dscli_profile_path for {0}".format(stg_name))
        exit()

    ds8k = pystorage.IBM.DS8K(config.dscli_bin,
                              config.dscli_profile_path + '/' + stg_sid)

    print('\nGetting the Volume Group and hostname used on storage ...'
          '\n\nPlease wait...')

    vol_group = ds8k.get_volgrpid(wwn_client)
    hostname_client_stg = ds8k.get_hostname(wwn_client)

    if (vol_group[0] != 0) or hostname_client_stg[0] != 0:
        print "{0} - {1}".format(vol_group[1], hostname_client_stg[1])
        exit(1)
    else:
        print('\nVolume Group from \033[1;32m{0}\033[1;00m identified '
              'as \033[1;32m{1}\033[1;00m.'.format(wwn_client, vol_group[1]))
        print('Hostname used on storage is '
              '\033[1;32m{0}\033[1;00m'.format(hostname_client_stg[1]))

    # select first and second pool

    print('\n[POOLS Selection]')
    print('\n\033[1;31mNOTE:\033[1;00m '
          'The Primary pool will be used for extra LUN if the number '
          'of LUNs is odd. '
          '\nExample: Total of LUNs = 11'
          '\n6 LUNs in Primary pool and 5 LUNs in the Secondary pool.\n'
          '\nPlease wait...')

    # pool informations
    ds8k_pools = ds8k.lsextpool()
    if ds8k_pools[0] != 0:
        print 'ERROR: {0}'.format(ds8k_pools[1])
        exit()
    else:
        print ds8k_pools[1]

    pool_list = []
    for l_pool in ds8k_pools[1].split('\n')[3:]:
        try:
            pool_list.append(l_pool.split()[0])
        except (IndexError, ValueError):
            pass

    # Primary Pool
    count = 0
    for l_pool in pool_list:
        print ('{0}: {1}'.format(count, l_pool))
        count += 1

    while True:
        try:
            pool_1_option = int(raw_input("Select Primary pool: "))
            break
        except (IndexError, ValueError):
            print(
                '\tERROR: Select an existing option between'
                '0 and {0}.'.format(count))

    pool_1_option = pool_list[pool_1_option]
    # cleaning the selected pool
    pool_list.remove(pool_1_option)
    print("\nPlease select the LUN LSS ID CODE "
          "to be used by {0}\n"
          "The code need to be between 00 and FF".format(pool_1_option))

    while True:
        try:
            code_1_pool = raw_input('Digit the LSS: ')
            int(code_1_pool, 16)
            if len(code_2_pool) != 2:
                print ("The code need to be between 00 and FF.")
            else:
                break
        except ValueError:
            print ("The code need to be between 00 and FF.")


    print("Primary pool: {0} | LUN ID Code: {1}\n".format(
        pool_1_option, code_1_pool))

    # Secondary Pool
    count = 0
    for l_pool in pool_list:
        print ('{0}: {1}'.format(count, l_pool))
        count += 1

    while True:
        try:
            pool_2_option = int(raw_input("Select Secondary pool: "))
            break
        except (IndexError, ValueError):
            print(
                '\tERROR: Select an existing option between '
                '0 and {0}.'.format(count))

    pool_2_option = pool_list[pool_2_option]

    print("\nPlease select the LUN LSS ID CODE "
          "to be used by {0}\n"
          "The code need to be between 00 and FF".format(pool_2_option))

    while True:
        try:
            code_2_pool = raw_input('Digit the LSS: ')
            int(code_2_pool, 16)
            if len(code_2_pool) != 2:
                print ("The code need to be between 00 and FF.")
            else:
                break
        except ValueError:
            print ("The code need to be between 00 and FF.")

    print("\n* Primary pool   : {0} | LUN ID Code: {1}XX\n"
          "* Secondary pool : {2} | LUN ID Code: {3}XX\n".format(pool_1_option,
                                                                 code_1_pool,
                                                                 pool_2_option,
                                                                 code_2_pool))
    print("\nPlease wait...")

    # disk count (number of disks)
    disk_count = disk_volume / lun_size
    if (disk_count % 2) != 0:
        disk_1_count = (disk_count / 2) + 1
        disk_2_count = (disk_count / 2)
    else:
        disk_1_count = (disk_count / 2)
        disk_2_count = (disk_count / 2)

    # getting free IDs for LSS Primary
    lss_free = getid.GetID(config.dscli_bin,
                           config.dscli_profile_path + '/' + stg_sid,
                           code_1_pool)

    lss_1_free = lss_free.free_lss()

    if len(lss_1_free) < disk_count:
        print(
            "ERROR: Not exist sufficient free IDs on {0} LSS.".format(
                code_1_pool))
        exit()

    lss_1_id_list = lss_1_free[:disk_1_count]

    # getting free IDs for LSS Secondary
    lss_free = getid.GetID(config.dscli_bin,
                           config.dscli_profile_path + '/' + stg_sid,
                           code_2_pool)

    lss_2_free = lss_free.free_lss()

    lss_2_id_list = lss_2_free[:disk_2_count]

    print ("Please give the SID (Code to identify) the LUNs.\n"
           "Use a name to identify the environment or client.\n"
           "Examples: DEV or MIGRATION or FOOBAR\n\n"
           "With this code the LUNs will be create as SID_LUN_SSL:\n"
           "Example: DEV_LUN_A601 or MIGRATION_LUN_AA07 or FOOBAR_LUN_045A\n")
    lun_sid = raw_input("LUN SID: ")

    new_change = ds8k_add_dev.New(change, hostname_client, storage_name,
                                  wwn_client, stg_name, stg_type, stg_sid,
                                  pool_1_option, pool_2_option, disk_1_count,
                                  disk_2_count, lss_1_id_list, lss_2_id_list,
                                  disk_volume, lun_size, lun_sid,
                                  vol_group[1], hostname_client_stg[1])
    new_change.preview()

    save_config = fields.YesNo('Do you would like save this allocation?[y/n]: ',
                               'n')
    save_config = save_config.check()

    if save_config == 'y':

        new_change.headerchange()
        new_change.writechange()
        end_change = new_change.closechange()
        print end_change

    else:
        print('Finishing. Thank you.')


def main_menu():
    global disk_volume, lun_size

    os.system('clear')
    print('')
    print('[ Storage Adm                           ]')
    print('[                                       ]')
    print('[ Version {0} - (c) 2016 Kairo Araujo ]'.format(globalvar.version))
    print('[ http://github.com/kairoaraujo/STGAdm  ]')
    print('[ BSD License                           ]')
    print('[                                       ]')

    stgadm = raw_input('\nMain Menu:\n\n'
                       '1. Add new volumes to existent host. (create change)\n'
                       '2. Execute changes created.\n'
                       '\nPlease choose an option: ')

    # Add new volumes to existent host menu

    if stgadm == '1':

        print('\n\n[ REQUEST INFORMATIONS ]\n')

        change = fields.Fields('change', 'Ticket/Change/Work Order: ')
        change.chkfieldstr()
        change = change.strvarout()

        hostname_client = fields.Fields('hostname', 'Hostname Client: ')
        hostname_client.chkfieldstr()
        hostname_client = hostname_client.strvarout()

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
                    '\nDo not use GB. Example: 1000 for 1000GB (1TB).')

        while True:
            try:
                lun_size = int(raw_input("Default LUN size (GB): "))

                if disk_volume % lun_size == 0:
                    break
                else:
                    print('\tERROR: The LUN size need to be a divisor of Total'
                          'required disk.'
                          '\n\t       If Total Disk Required is wrong, please '
                          'use "Ctrl+C".')
            except (TypeError, ValueError):
                print(
                    '\tERROR: LUN Size need to be an int value.'
                    '\nDo not use GB. Example 100 for 100GB size of LUNs.')

        if ':' in wwn_client:
            wwn_client = wwn_client.replace(':', '')

        # select storage
        get_stg = systemstorages.SystemStorages()
        get_stg.selectstorage()

        stg_type = get_stg.gettype()

        if stg_type == 'EMC_VMAX':
            stg_sid = get_stg.getsid()
            stg_name = get_stg.getstorage()
            storage_name = stg_name
            menu_emc_vmax(change, hostname_client, storage_name, stg_name,
                          stg_type, stg_sid, wwn_client)

        elif stg_type == 'IBM_DS8K':
            stg_sid = get_stg.getsid()
            stg_name = get_stg.getstorage()
            storage_name = stg_name
            menu_ibm_ds8k(change, hostname_client, storage_name, stg_name,
                          stg_type, stg_sid, wwn_client)

        elif stg_type == 'EMC_VNX':
            pass

        else:
            print('ERROR: Storage type {0} invalid. Check config file'.format(
                stg_type))

    elif stgadm == '2':

        change_file = findchange.select().replace('.py', '')
        os.system('python -c \"import stgadm.changes.{0}; '
                  'stgadm.changes.{0}.preview()\"'
                  .format(change_file))

        execute_change = fields.YesNo('Do you would like execute this '
                                      'change?[y/n]: ', 'n')
        execute_change = execute_change.check()

        if execute_change == 'y':
            print "Executing the change. Please wait...\n"

            os.system('python -c \"import stgadm.changes.{0}; '
                      'stgadm.changes.{0}.execute()\"'
                      .format(change_file))

            orig_change = '{0}/stgadm/changes/{1}.py'.format(config.stghome,
                                                             change_file)
            dest_change = '{0}/stgadm/changes_executed/{1}.py'.format(
                config.stghome, change_file)

            os.rename(orig_change, dest_change)

    else:
        print 'Wrong option. Exiting.'
