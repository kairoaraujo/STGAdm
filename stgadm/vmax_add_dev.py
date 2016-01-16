#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import config
import globalvar
import emc_cmds
import shutil


class New:

    def __init__(self, change=None, hostname_client=None, storage_name=None,
                 wwn_client=None, stg_name=None, stg_type=None, stg_sid=None,
                 ign=None, mvn=None, sgn=None, stg_pool=None, disk_volume=None,
                 lun_size=None, lun_type=None, member_meta_size=None,
                 disk_count=None):
        self.change = change
        self.hostname_client = hostname_client
        self.storage_name = storage_name
        self.wwn_client = wwn_client
        self.stg_name = stg_name
        self.stg_type = stg_type
        self.stg_sid = stg_sid
        self.ign = ign
        self.mvn = mvn
        self.sgn = sgn
        self.stg_pool = stg_pool
        self.disk_volume = disk_volume
        self.lun_size = lun_size
        self.lun_type = lun_type
        self.member_meta_size = member_meta_size
        self.disk_count = disk_count

    def preview(self):
        print('\nConfig validation\n')
        print('\nClient Information')
        print(50 * '-')
        print('Register      : {0}'.format(self.change))
        print('Client Server : {0}'.format(self.hostname_client))
        print('Storage Name  : {0}'.format(self.storage_name))
        print('WWN Client    : {0}'.format(self.wwn_client))
        print('\nStorage Information')
        print(50 * '-')
        print('Storage Name          : {0}'.format(self.stg_name))
        print('Storage Type          : {0}'.format(self.stg_type))
        print('Storage SID           : {0}'.format(self.stg_sid))
        print('Initiator Group Name  : {0}'.format(self.ign))
        print('Making View Names     : {0}'.format(self.mvn))
        print('Storage Group Name    : {0}'.format(self.sgn))
        print('Storage Pool          : {0}'.format(self.stg_pool))
        print('\nInformations about the request:')
        print(50 * '-')
        print('Disk Volume   : {0}GB'.format(self.disk_volume))
        print('LUN Size      : {0}GB'.format(self.lun_size))
        print('Device type   : {0}GB'.format(self.lun_type))
        if self.lun_type == 'meta':
            print('Member Size   : {0}GB (meta)'.format(self.member_meta_size))
        print('DiskCount         : {0}'.format(self.disk_count))
        print(50 * '-')
        print('\n')

    def execute(self):
        exec_change = emc_cmds.VMAX(config.symcli_path, self.stg_sid)
        exec_return = exec_change.create_dev(self.disk_count,
                                             self.lun_size,
                                             self.member_meta_size,
                                             self.lun_type,
                                             self.stg_pool,
                                             self.sgn)

        return exec_return

    def headerchange(self):
        """ Write the header of file. """

        global file_change

        file_change = open(
            '{0}/stgadm/tmp/{1}_{2}_{3}.py'.format(config.stghome, self.change,
                                                   self.ign,
                                                   globalvar.timestr), 'w')

        file_change.write(
            '#!/usr/bin/env python\n'
            '# -*- coding: utf-8 -*-\n'
            '#'
            '# Time: {0}'
            '#\n'
            '\n'.format(globalvar.timestr)
        )

    def writechange(self):
        """ Write the body of file. """

        #
        # config functions to write correct action to lpar
        #

        file_change.write(
            "\n"
            "#import \n"
            "\n"
            "import vmax_add_dev\n"
            "\n"
            "# variables\n"
            "change = {0}\n"
            "hostname_client = {1}\n"
            "storage_name = {2}\n"
            "wwn_client = {3}\n"
            "stg_name = {4}\n"
            "stg_type = {5}\n"
            "stg_sid = {6}\n"
            "ign = {7}\n"
            "mvn = {8}\n"
            "sgn = {9}\n"
            "stg_pool = {10}\n"
            "disk_volume = {11}\n"
            "lun_size = {12}\n"
            "lun_type = {13}\n"
            "member_meta_size = {14}\n"
            "disk_count = {15}\n"
            "timestr = {16}\n"
            "\n"
            "\n "
            "{0}_{7}_{16} = vmax_add_dev("
            "                       change, hostname_client, storage_name,\n"
            "                       wwn_client, stg_name, stg_type, stg_sid,\n"
            "                       ign, mvn, sgn, stg_pool, disk_volume,\n"
            "                       lun_size, lun_type, member_meta_size,\n"
            "                       disk_count\n"
            "\n"
            "def preview(self):\n"
            "\n\t"
            "\t{0}_{7}_{16}.preview()"
            "\n\t"
            "\n"
            "def preview(self):\n"
            "\n\t"
            "\n"
            "\tevidence = {0}_{7}_{16}.execute()\n"
            "\tprint evidence"
            "\n"
            "\n".format(
                self.change,
                self.hostname_client,
                self.storage_name,
                self.wwn_client,
                self.stg_name,
                self.stg_type,
                self.stg_sid,
                self.ign,
                self.mvn,
                self.sgn,
                self.stg_pool,
                self.disk_volume,
                self.lun_size,
                self.lun_type,
                self.member_meta_size,
                globalvar.timestr
            )
        )

    def closechange(self):
        """ Close the file and move to correct directory """

        file_change.write('\n\n# File closed with success by STGAdm.\n')
        file_change.close()
        shutil.move('{0}/stgadm/tmp/{1}_{2}_{3}.py',
                    '{0}/stgadm/changes/{1}_{2}_{3}.py'.format(
                        config.stghome, self.change, self.ign,
                        globalvar.timestr))

        return ('{0}/stgadm/changes/{1}_{2}_{3}.py'.format(
            config.stghome, self.change, self.ign,
            globalvar.timestr))