# !/usr/bin/env python  # -*- coding: utf-8 -*-
#
#
import config
import globalvar
import pystorage
import os


class New:
    def __init__(self, change=None, hostname_client=None, storage_name=None,
                 wwn_client=None, stg_name=None, stg_type=None, stg_sid=None,
                 pool_1_option=None, pool_2_option=None, disk_1_count=None,
                 disk_2_count=None, lss_1_id_list=None, lss_2_id_list=None,
                 disk_volume=None, lun_size=None, lun_sid=None,
                 vol_group=None, hostname_client_stg=None, disk_count=None,
                 cls=None, cls_nodes=None):

        self.change = change
        self.hostname_client = hostname_client
        self.storage_name = storage_name
        self.wwn_client = wwn_client
        self.stg_name = stg_name
        self.stg_type = stg_type
        self.stg_sid = stg_sid
        self.pool_1_option = pool_1_option
        self.pool_2_option = pool_2_option
        self.disk_1_count = disk_1_count
        self.disk_2_count = disk_2_count
        self.lss_1_id_list = lss_1_id_list
        self.lss_2_id_list = lss_2_id_list
        self.disk_volume = disk_volume
        self.lun_size = lun_size
        self.lun_sid = lun_sid
        self.vol_group = vol_group
        self.hostname_client_stg = hostname_client_stg
        self.disk_count = disk_count
        self.cls = cls
        self.cls_nodes = cls_nodes
        self.time = globalvar.timestr.replace('-', '_')

        self.lun_1_list = []
        for l_lun in self.lss_1_id_list:
            self.lun_1_list.append('{0}_{1}'.format(self.lun_sid, l_lun))

        self.lun_2_list = []
        for l_lun in self.lss_2_id_list:
            self.lun_2_list.append('{0}_{1}'.format(self.lun_sid, l_lun))

        self.ds8k = pystorage.DS8K(config.dscli_bin,
                                   config.dscli_profile_path + '/' +
                                   self.stg_sid)

    def _lun_availability(self, lun_list):
        return_msg_free = 'CMUC00234I lsfbvol: No FB Volume found.'

        for lun in lun_list:
            if self.ds8k.lsfbvol(lun)[1].split('\n')[1] == return_msg_free:
                print ("LUN {0} is available to create.".format(lun))

            else:
                print ("ERROR: LUN {0} is not longer available.".format(lun))
                print ("       This change is automatically canceled!")
                raise ValueError("InvalidLUNId")

    def preview(self):

        print('\nConfig validation\n')
        print('\033[1;34m\nClient Information:\033[1;00m')
        print(90 * '-')
        print('Register                   : {0}'.format(self.change))
        print('Client Server              : {0}'.format(self.hostname_client))
        print('Storage Name               : {0}'.format(self.storage_name))
        print('Hostname client on Storage : {0}'.format(
            self.hostname_client_stg))
        print('Storage Volume Group       : {0}'.format(self.vol_group))
        print('WWN Client                 : {0}'.format(self.wwn_client))
        print('\033[1;34m\nStorage Information:\033[1;00m')
        print(90 * '-')
        print('Storage Name   : {0}'.format(self.stg_name))
        print('Storage Type   : {0}'.format(self.stg_type))
        print('Storage SID    : {0}'.format(self.stg_sid))
        print('Pool Primary   : {0} *LSS IDs: {1}'.format(
            self.pool_1_option, self.lss_1_id_list))
        print('\_ LUNs:       : {0}'.format(self.lun_1_list))
        print('Pool Secondary : {0} *LSS IDs: {1}'.format(
            self.pool_2_option, self.lss_2_id_list))
        print('\_ LUNs:       : {0}'.format(self.lun_2_list))
        print('\033[1;34m\nInformations about the request:\033[1;00m')
        print(90 * '-')
        print('Disk Volume   : {0}GB'.format(self.disk_volume))
        print('LUN Size      : {0}GB'.format(self.lun_size))
        print('Disk Count    : {0}'.format(
            self.disk_1_count + self.disk_2_count))
        if self.cls == 'y':
            print('\033[1;34m\nCluster Information:\033[1;00m')
            print(90 * '-')
            print('Cluster LUNs ([Primary POOL] | [Secondary POOL]):')
            print('{0} | {1}'.format(
                self.lun_1_list, self.lun_2_list))
            for key in self.cls_nodes:
                print('\nCluster Node information {0}:'.format(key))
                print('+ Hostname client on Storage : {0}'.format(
                    self.cls_nodes[key][0]))
                print('+ Storage Volume Group       : {0}'.format(
                    self.cls_nodes[key][1]))
                print('+ WWPN Address               : {0}'.format(
                    self.cls_nodes[key][2]))
        print('\n')
        print('Checking LUNs availability...')
        print('Please wait the finish message.\n')

        try:
            self._lun_availability(self.lss_1_id_list)
        except ValueError, e:
            raise ValueError(e)

        if len(self.lss_2_id_list) > 0:
            try:
                self._lun_availability(self.lss_2_id_list)
            except ValueError, e:
                raise ValueError(e)

        print ('\nLUN availability finished.\n')

    def execute(self):

        global exec_return, evidence_file_name

        # init the evidence header
        evidence_file_name = '{0}/stgadm/evidences/{1}_{2}_{3}.txt'.format(
            config.stghome, self.change, self.vol_group, self.time)

        evidence_file = open(evidence_file_name, 'w')
        evidence_file.write(
            "# EVIDENCE FILE \n"
            "#\n"
            "# Change/Ticket/WO: {0}\n"
            "##############################################################\n"
            "\n".format(self.change)

        )
        evidence_file.close()

        # write evidence
        def _write_evidence(output_data, file_name):
            """ Write the output data on file

                :param output_data: this is a array with return code and output
                                    [return code, output data]
                """

            f_evidence_file = open(file_name, 'a')

            f_evidence_file.write(
                "# Command Return code: {0}\n"
                "\n"
                "# Output:\n"
                "{1}\n".format(output_data[0], output_data[1]))

            f_evidence_file.close()

        def _remove_reserved_id(lun_id):
            """ Clear ID from reserved_ids.db

                :lun_id: array if with LUN IDs
                """

            reserved_ids = open(
                '{0}/stgadm/data/reserved_ids.db'.format(config.stghome), 'r')
            line_reservedids = reserved_ids.readlines()
            reserved_ids.close()
            reserved_ids = open(
                '{0}/stgadm/data/reserved_ids.db'.format(config.stghome), 'w')
            for lineids in line_reservedids:
                reserved_ids.write(lineids.replace(lun_id + '\n', ''))
            reserved_ids.close()

        evidence_file = open(evidence_file_name, 'a')
        evidence_file.write("# CREATING/ALLOCATION LUN(s)\n"
                            "############################\n".format(
            self.vol_group))
        evidence_file.close()

        for l_id in self.lss_1_id_list:
            exec_return = self.ds8k.mkfbvol(self.pool_1_option, self.lun_size,
                                            self.lun_sid,
                                            self.vol_group, l_id)

            _write_evidence(exec_return, evidence_file_name)
            _remove_reserved_id(l_id)

        if self.disk_count > 1:
            for l_id in self.lss_2_id_list:
                exec_return = self.ds8k.mkfbvol(self.pool_2_option,
                                                self.lun_size,
                                                self.lun_sid,
                                                self.vol_group, l_id)

                _write_evidence(exec_return, evidence_file_name)
                _remove_reserved_id(l_id)

        # write the status of volume group
        evidence_file = open(evidence_file_name, 'a')
        evidence_file.write("# LUN list for Volume Group {0}\n".format(
            self.vol_group))
        evidence_file.close()

        exec_return = self.ds8k.lsfbvol('-volgrp {0}'.format(
            self.vol_group))

        _write_evidence(exec_return, evidence_file_name)

        if self.cls == 'y':

            evidence_file = open(evidence_file_name, 'a')
            evidence_file.write("# CLUSTER NODE (adding LUN(s))\n"
                                "##############################\n")
            evidence_file.close()

            for cluster_node in self.cls_nodes.keys():

                evidence_file = open(evidence_file_name, 'a')
                evidence_file.write("# Adding LUN(s) for Cluster node {0} "
                                    "[Volume Group {1}]\n".format(
                    self.cls_nodes[cluster_node][0],
                    self.cls_nodes[cluster_node][1]))
                evidence_file.close()

                for l_id in self.lss_1_id_list:
                    exec_return = self.ds8k.chvolgrp(
                        l_id,
                        self.cls_nodes[cluster_node][1]
                    )

                    _write_evidence(exec_return, evidence_file_name)

                for l_id in self.lss_2_id_list:
                    exec_return = self.ds8k.chvolgrp(
                        l_id,
                        self.cls_nodes[cluster_node][1]
                    )

                    _write_evidence(exec_return, evidence_file_name)

                evidence_file = open(evidence_file_name, 'a')
                evidence_file.write("# LUN list for Volume Group {0}\n".format(
                    self.vol_group))
                evidence_file.close()
                exec_return = self.ds8k.lsfbvol('-volgrp {0}'.format(
                    self.cls_nodes[cluster_node][1]
                ))
                _write_evidence(exec_return, evidence_file_name)

        return evidence_file_name

    def headerchange(self):
        """ Write the header of file. """

        global file_change

        file_change = open(
            '{0}/stgadm/tmp/change_{1}_{2}_{3}_{4}.py'.format(
                config.stghome,
                self.change,
                self.hostname_client_stg,
                self.vol_group,
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

        file_change.write(
            "\n"
            "# import \n"
            "\n"
            "from stgadm import ds8k_add_dev\n"
            "\n"
            "# variables\n"
            "change = '{0}'\n"
            "hostname_client = '{1}'\n"
            "storage_name = '{2}'\n"
            "wwn_client = '{3}'\n"
            "stg_name = '{4}'\n"
            "stg_type = '{5}'\n"
            "stg_sid = '{6}'\n"
            "pool_1_option = '{7}'\n"
            "pool_2_option = '{8}'\n"
            "disk_1_count = {9}\n"
            "disk_2_count = {10}\n"
            "lss_1_id_list = {11}\n"
            "lss_2_id_list = {12}\n"
            "disk_volume = {13}\n"
            "lun_size = {14}\n"
            "lun_sid = '{15}'\n"
            "vol_group = '{16}'\n"
            "hostname_client_stg = '{17}'\n"
            "disk_count = {18}\n"
            "cls = '{19}'   \n"
            "cls_nodes = {20}\n"
            "time = '{21}'\n"

            "\n"
            "\n"
            "{0}_{7}_{17}_{21} = ds8k_add_dev.New(\n"
            "               change, hostname_client, storage_name,\n"
            "               wwn_client, stg_name, stg_type, stg_sid,\n"
            "               pool_1_option, pool_2_option, disk_1_count,\n"
            "               disk_2_count, lss_1_id_list, lss_2_id_list,\n"
            "               disk_volume, lun_size, lun_sid,\n"
            "               vol_group, hostname_client_stg, disk_count,\n"
            "               cls, cls_nodes)\n"
            "\n"
            "def preview():\n"
            "    \n"
            "    {0}_{7}_{17}_{21}.preview()\n"
            "    \n"
            "    \n"
            "def execute():\n"
            "    \n"
            "    \n"
            "    evidence = {0}_{7}_{17}_{21}.execute()\n"
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
                self.pool_1_option,  # 7
                self.pool_2_option,  # 8
                self.disk_1_count,  # 9
                self.disk_2_count,  # 10
                self.lss_1_id_list,  # 11
                self.lss_2_id_list,  # 12
                self.disk_volume,  # 13
                self.lun_size,  # 14
                self.lun_sid,  # 15
                self.vol_group,  # 16
                self.hostname_client_stg,  # 17
                self.disk_count,  # 18
                self.cls,  # 19
                self.cls_nodes,  # 20
                self.time))  # 21

    def closechange(self):
        """ Close the file and move to correct directory """

        file_change.write('\n# File closed with success by STGAdm.\n')
        file_change.close()

        orig_change = '{0}/stgadm/tmp/change_{1}_{2}_{3}_{4}.py'.format(
            config.stghome,
            self.change,
            self.hostname_client_stg,
            self.vol_group,
            self.time)

        dest_change = '{0}/stgadm/changes/change_{1}_{2}_{3}_{4}.py'.format(
            config.stghome,
            self.change,
            self.hostname_client_stg,
            self.vol_group,
            self.time)

        os.rename(orig_change, dest_change)

        if os.path.isfile(
                '{0}/stgadm/data/reserved_ids.db'.format(config.stghome)):
            reserve_ids_file = open(
                '{0}/stgadm/data/reserved_ids.db'.format(config.stghome), 'a')
            for l_ids in self.lss_1_id_list:
                reserve_ids_file.write(l_ids + '\n')
            for l_ids in self.lss_2_id_list:
                reserve_ids_file.write(l_ids + '\n')
            reserve_ids_file.close()

        if os.path.isfile(dest_change):
            return 'The change {0} was successfully save.'.format(dest_change)
