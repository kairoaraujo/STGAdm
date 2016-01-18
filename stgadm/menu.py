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
import vmax_add_dev
import findchange


def menu_emc_vmax(change=None, hostname_client=None, storage_name=None,
                  stg_name=None, stg_type=None, stg_sid=None, wwn_client=None):
    # get storage informations
    global pool_option

    chk_server = emc_cmds.VMAX(config.symcli_path, stg_sid)

    print('\nCollecting some storage informations. Please wait...')

    ign = chk_server.get_ign(wwn_client)

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
        except IndexError:
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

    save_config = fields.YesNo('Do you would like save this allocation?: ',
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
    print('[ Storage Adm ]\n[ Version {0} - © 2015 ]\n\n'.format(
        globalvar.version))

    stgadm = raw_input('STG Adm options\n\n'
                       '1. Add new volumes to existent host. (create change)\n'
                       '2. Execute changes created\n'
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

        stg_type = get_stg.gettype()

        if stg_type == 'EMC_VMAX':
            stg_sid = get_stg.getsid()
            stg_name = get_stg.getstorage()
            menu_emc_vmax(change, hostname_client, storage_name, stg_name,
                          stg_type, stg_sid, wwn_client)

        elif stg_type == 'EMC_VNX':
            pass

        else:
            print('ERRO: Storage type {0} invalid. Check config file'.format(
                stg_type))

    elif stgadm == '2':

        change_file = findchange.select()
        os.system('python -c \"import changes.{0}; \"changes.{0}.preview()'
                  .format(change_file))
        execute = fields.YesNo('Do you would like execute this change?: ',
                               'n')
        if execute == 'y':
            os.system('python -c \"import changes.{0}; \"changes.{0}.execute()'
                      .format(change_file))

            orig_change = '{0}/stgadm/changes/{1}'.format(config.stghome,
                                                          change_file)
            dest_change = '{0}/stgadm/changes_executed/{1}'.format(
                config.stghome, change_file)

            os.rename(orig_change, dest_change)

    else:
        print 'Wrong option. Exiting.'
