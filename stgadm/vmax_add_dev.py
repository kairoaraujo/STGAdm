#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import config
import globalvar
import pystorage
import os


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
        self.time = globalvar.timestr.replace('-', '_')

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
        print('Device type   : {0}'.format(self.lun_type))
        if self.lun_type == 'meta':
            print('Member Size   : {0}GB (meta)'.format(self.member_meta_size))
        print('Disk Count    : {0}'.format(self.disk_count))
        print(50 * '-')
        print('\n')

    def execute(self):
        exec_change = pystorage.EMC.VMAX(config.symcli_path)
        exec_return = exec_change.create_dev(self.stg_sid,
                                             self.disk_count,
                                             self.lun_size,
                                             self.member_meta_size,
                                             self.lun_type,
                                             self.stg_pool,
                                             self.sgn)

        file_name = '{0}/stgadm/evidences/{1}_{2}_{3}.txt'.format(
            config.stghome, self.change, self.ign, self.time)
        evidence_file = open(file_name, 'w')

        evidence_file.write(
            "# Evidence\n"
            "#\n"
            "\n"
            "Return code: {0}\n"
            "\n"
            "Output:\n"
            "{1}\n".format(exec_return[0], exec_return[1])
        )

        evidence_file.close()

        return file_name

    def headerchange(self):
        """ Write the header of file. """

        global file_change

        file_change = open(
            '{0}/stgadm/tmp/change_{1}_{2}_{3}.py'.format(config.stghome,
                                                          self.change,
                                                          self.ign,
                                                          self.time), 'w')

        file_change.write(
            '#!/usr/bin/env python\n'
            '# -*- coding: utf-8 -*-\n'
            '#\n'
            '# Time: {0}\n'
            '#\n'
            '\n'.format(self.time)
        )

    def writechange(self):
        """ Write the body of file. """

        #
        # config functions to write correct action to lpar
        #

        file_change.write(
            "\n"
            "# import \n"
            "\n"
            "from stgadm import vmax_add_dev\n"
            "\n"
            "# variables\n"
            "change = '{0}'\n"
            "hostname_client = '{1}'\n"
            "storage_name = '{2}'\n"
            "wwn_client = '{3}'\n"
            "stg_name = '{4}'\n"
            "stg_type = '{5}'\n"
            "stg_sid = '{6}'\n"
            "ign = '{7}'\n"
            "mvn = '{8}'\n"
            "sgn = '{9}'\n"
            "stg_pool = '{10}'\n"
            "disk_volume = '{11}'\n"
            "lun_size = {12}\n"
            "lun_type = '{13}'\n"
            "member_meta_size = {14}\n"
            "disk_count = {15}\n"
            "time = '{16}'\n"
            "\n"
            "\n"
            "{0}_{7}_{16} = vmax_add_dev.New(\n"
            "                       change, hostname_client, storage_name,\n"
            "                       wwn_client, stg_name, stg_type, stg_sid,\n"
            "                       ign, mvn, sgn, stg_pool, disk_volume,\n"
            "                       lun_size, lun_type, member_meta_size,\n"
            "                       disk_count)\n"
            "\n"
            "def preview():\n"
            "    \n"
            "    {0}_{7}_{16}.preview()\n"
            "    \n"
            "    \n"
            "def execute():\n"
            "    \n"
            "    \n"
            "    evidence = {0}_{7}_{16}.execute()\n"
            "    print('\\nChange executed!')\n"
            "    evidence_file=open(evidence)\n"
            "    print(evidence_file.read())\n"
            "    evidence_file.close()\n"
            "    print('\\nAll evidences are in {{0}}\\n'"
            ".format(evidence))\n"
            "    \n"
            "    \n".format(
                self.change,  # 0
                self.hostname_client,  # 1
                self.storage_name,  # 2
                self.wwn_client,  # 3
                self.stg_name,  # 4
                self.stg_type,  # 5
                self.stg_sid,  # 6
                self.ign,  # 7
                self.mvn,  # 8
                self.sgn,  # 9
                self.stg_pool,  # 10
                self.disk_volume,  # 11
                self.lun_size,  # 12
                self.lun_type,  # 13
                self.member_meta_size,  # 14
                self.disk_count,  # 15
                self.time))  # 16)

    def closechange(self):
        """ Close the file and move to correct directory """

        file_change.write('\n# File closed with success by STGAdm.\n')
        file_change.close()

        orig_change = '{0}/stgadm/tmp/change_{1}_{2}_{3}.py'.format(
            config.stghome, self.change, self.ign, self.time)

        dest_change = '{0}/stgadm/changes/change_{1}_{2}_{3}.py'.format(
            config.stghome, self.change, self.ign, self.time)

        os.rename(orig_change, dest_change)

        if os.path.isfile(dest_change):
            return 'The change {0} was successfully save.'.format(dest_change)

