# !/usr/bin/env python
#  -*- coding: utf-8 -*-
#
#
import config
import globalvar
import pystorage
import os


def remove_reserved_id(lun_id):
    """ Clear ID from reserved_ids.db
        :param lun_id: array if with LUN IDs
        """
    reserved_ids = open(
        '{0}/stgadm/data/vnx_reserved_ids.db'.format(config.stghome),
        'r')
    line_reservedids = reserved_ids.readlines()
    reserved_ids.close()
    reserved_ids = open(
        '{0}/stgadm/data/vnx_reserved_ids.db'.format(config.stghome),
        'w')
    for lineids in line_reservedids:
        reserved_ids.write(lineids.replace('{0}\n'.format(lun_id), ''))
    reserved_ids.close()


def remove_reserved_hlu_id(hlu_id, stggroup_name):
    """ Clear ID from reserved_ids.db
        :param hlu_id: The HLU ID
        :param stggroup_name: The storage group name from HLU
        """
    reserved_ids = open(
        '{0}/stgadm/data/vnx_reserved_hlu_{1}.db'.format(
            config.stghome, stggroup_name),
        'r')
    line_reservedids = reserved_ids.readlines()
    reserved_ids.close()
    reserved_ids = open(
        '{0}/stgadm/data/vnx_reserved_hlu_{1}.db'.format(
            config.stghome, stggroup_name),
        'w')
    for lineids in line_reservedids:
        reserved_ids.write(lineids.replace('{0}\n'.format(hlu_id), ''))
    reserved_ids.close()


class New:
    def __init__(self, change=None, hostname_client=None, storage_name=None,
                 wwn_client=None, stg_name=None, stg_type=None, stg_1ip=None,
                 stg_2ip=None, stg_user=None, stg_pass=None, stg_scope=None,
                 stg_pool=None, disk_count=None, lu_ids=None, hlu_ids=None,
                 disk_volume=None, lun_size=None, lun_sid=None,
                 hostname_client_storage=None, stggroup_name=None,
                 lun_type=None, cls=None, cls_nodes=None):

        self.change = change
        self.hostname_client = hostname_client
        self.storage_name = storage_name
        self.wwn_client = wwn_client
        self.stg_name = stg_name
        self.stg_type = stg_type
        self.stg_1ip = stg_1ip
        self.stg_2ip = stg_2ip
        self.stg_user = stg_user
        self.stg_pass = stg_pass
        self.stg_scope = stg_scope
        self.stg_pool = stg_pool
        self.disk_count = disk_count
        self.lu_ids = lu_ids
        self.hlu_ids = hlu_ids
        self.disk_volume = disk_volume
        self.lun_size = lun_size
        self.lun_sid = lun_sid
        self.hostname_client_storage = hostname_client_storage
        self.stggroup_name = stggroup_name
        self.lun_type = lun_type
        self.cls = cls
        self.cls_nodes = cls_nodes
        self.time = globalvar.timestr.replace('-', '_')

        self.lun_list = []
        for l_lun in self.lu_ids:
            self.lun_list.append('{0}_LUN_{1}'.format(self.lun_sid, l_lun))

        self.vnx = pystorage.VNX(config.naviseccli_bin, self.stg_1ip,
                                 self.stg_2ip, self.stg_user, self.stg_pass,
                                 self.stg_scope)

    def _lun_availability(self, lun_list):
        for lun in lun_list:
            if self.vnx.show_lun(lun)[0] == 9:
                print ("LUN {0} is available to create.".format(lun))

            else:
                print ("ERROR: LUN {0} is not longer available.".format(lun))
                print ("       This change is automatically canceled!")
                raise ValueError("InvalidLUNId")

    def _hlu_availability(self, hlu_list, storage_group):
        fresh_hlu = self.vnx.get_hlu_stggroup(storage_group)

        if fresh_hlu[0] != 0:
            exit()
        else:
            fresh_hlu = fresh_hlu[1]
            fresh_hlu = map(int, fresh_hlu)

        for hlu in hlu_list:
            if hlu in fresh_hlu:
                print (
                    "ERROR: HLU {0} is not longer available for "
                    "Storage Group {1}".format(
                        hlu,
                        storage_group))
                print ("       This change is automatically canceled!")
                raise ValueError("InvalidHLUId")

            else:
                print (
                    "HLU {0} is available to create for "
                    "Storage Group {1}.".format(
                        hlu, storage_group))

    def headerchange(self):
        """ Write the header of file. """

        global file_change

        file_change = open(
            '{0}/stgadm/tmp/change_{1}_{2}_{3}_{4}.py'.format(
                config.stghome,
                self.change,
                self.hostname_client_storage,
                self.stggroup_name,
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
            "from stgadm import vnx_add_dev\n"
            "\n"
            "# variables\n"
            "change = '{0}'\n"
            "hostname_client = '{1}'\n"
            "storage_name = '{2}'\n"
            "wwn_client = '{3}'\n"
            "stg_name = '{4}'\n"
            "stg_type = '{5}'\n"
            "stg_1ip = '{6}'\n"
            "stg_2ip = '{7}'\n"
            "stg_user = '{8}'\n"
            "stg_pass = '{9}'\n"
            "stg_scope = '{10}'\n"
            "stg_pool = '{11}'\n"
            "disk_count = {12}\n"
            "lu_ids = {13}\n"
            "hlu_ids = {14}\n"
            "disk_volume = {15}\n"
            "lun_size = {16}\n"
            "lun_sid = '{17}'\n"
            "hostname_client_storage = '{18}'\n"
            "stggroup_name = '{19}'\n"
            "lun_type = '{20}'\n"
            "cls = '{21}'\n"
            "cls_nodes = {22}\n"
            "time = '{23}'\n"

            "\n"
            "\n"
            "{0}_{23} = vnx_add_dev.New(\n"
            "               change, hostname_client, storage_name,\n"
            "               wwn_client, stg_name, stg_type, stg_1ip,\n"
            "               stg_2ip, stg_user, stg_pass, stg_scope,\n"
            "               stg_pool, disk_count, lu_ids, hlu_ids,\n"
            "               disk_volume, lun_size, lun_sid,\n"
            "               hostname_client_storage, stggroup_name,\n"
            "               lun_type, cls, cls_nodes)\n"
            "\n"
            "def preview():\n"
            "    \n"
            "    {0}_{23}.preview()\n"
            "    \n"
            "    \n"
            "def execute():\n"
            "    \n"
            "    \n"
            "    evidence = {0}_{23}.execute()\n"
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
                self.stg_1ip,  # 6
                self.stg_2ip,  # 7
                self.stg_user,  # 8
                self.stg_pass,  # 9
                self.stg_scope,  # 10
                self.stg_pool,  # 11
                self.disk_count,  # 12
                self.lu_ids,  # 13
                self.hlu_ids,  # 14
                self.disk_volume,  # 15
                self.lun_size,  # 16
                self.lun_sid,  # 17
                self.hostname_client_storage,  # 18
                self.stggroup_name,  # 19
                self.lun_type,  # 20
                self.cls,  # 21
                self.cls_nodes,  # 22
                self.time))  # 23

    def closechange(self):
        """ Close the file and move to correct directory """

        file_change.write('\n# File closed with success by STGAdm.\n')
        file_change.close()

        orig_change = '{0}/stgadm/tmp/change_{1}_{2}_{3}_{4}.py'.format(
            config.stghome,
            self.change,
            self.hostname_client_storage,
            self.stggroup_name,
            self.time)

        dest_change = '{0}/stgadm/changes/change_{1}_{2}_{3}_{4}.py'.format(
            config.stghome,
            self.change,
            self.hostname_client_storage,
            self.stggroup_name,
            self.time)
        os.rename(orig_change, dest_change)

        # VNX reserved lu ids
        if os.path.isfile(
                '{0}/stgadm/data/vnx_reserved_ids.db'.format(config.stghome)):
            reserve_ids_file = open(
                '{0}/stgadm/data/vnx_reserved_ids.db'.format(config.stghome),
                'a')
            for l_ids in self.lu_ids:
                reserve_ids_file.write('{0}\n'.format(l_ids))
            reserve_ids_file.close()

        # VNX reserved hlu ids
        reserve_ids_file = open(
            '{0}/stgadm/data/vnx_reserved_hlu_{1}.db'.format(
                config.stghome, self.stggroup_name), 'a')
        for l_ids in self.hlu_ids:
            reserve_ids_file.write('{0}\n'.format(l_ids))
        reserve_ids_file.close()

        # VNX reserved hlu in case of cluster
        if self.cls == 'y':

            for cluster_node in self.cls_nodes.keys():
                for l_ids in self.cls_nodes[cluster_node][3]:
                    reserve_ids_file = open(
                        '{0}/stgadm/data/vnx_reserved_hlu_{1}.db'.format(
                            config.stghome,
                            self.cls_nodes[cluster_node][1]), 'a')
                    reserve_ids_file.write('{0}\n'.format(l_ids))
                reserve_ids_file.close()

        if os.path.isfile(dest_change):
            return 'The change {0} was successfully save.'.format(dest_change)

    def preview(self):

        print('\nConfig validation\n')
        print('\033[1;34m\nClient Information:\033[1;00m')
        print(90 * '-')
        print('Register                   : {0}'.format(self.change))
        print('Client Server              : {0}'.format(self.hostname_client))
        print('Storage Name               : {0}'.format(self.storage_name))
        print('Hostname client on Storage : {0}'.format(
            self.hostname_client_storage))
        print('Storage Volume Group       : {0}'.format(self.stggroup_name))
        print('\_ HLU IDs:                : {0}'.format(self.hlu_ids))
        print('WWN Client                 : {0}'.format(self.wwn_client))
        print('\033[1;34m\nStorage Information:\033[1;00m')
        print(90 * '-')
        print('Storage Name   : {0}'.format(self.stg_name))
        print('Storage Type   : {0}'.format(self.stg_type))
        print('Storage SID    : {0}, {1}'.format(self.stg_1ip, self.stg_2ip))
        print('Pool           : {0}'.format(self.stg_pool))
        print('\_ LUN Names   : {0}'.format(self.lun_list))
        print('\_ LUN IDs     : {0}'.format(self.lu_ids))
        print('\033[1;34m\nInformations about the request:\033[1;00m')
        print(90 * '-')
        print('Disk Volume   : {0}GB'.format(self.disk_volume))
        print('LUN Size      : {0}GB'.format(self.lun_size))
        print('Disk Count    : {0}'.format(self.disk_count))
        if self.cls == 'y':
            print('\033[1;34m\nCluster Information:\033[1;00m')
            print(90 * '-')
            print('Cluster LUNs:')
            print('{0}'.format(self.lu_ids))
            for key in self.cls_nodes:
                print('\nCluster Node information {0}:'.format(key))
                print('+ Hostname client on Storage : {0}'.format(
                    self.cls_nodes[key][0]))
                print('+ Storage Volume Group       : {0}'.format(
                    self.cls_nodes[key][1]))
                print('\_ HLU IDs                   : {0}'.format(
                    self.cls_nodes[key][3]))
                print('+ WWPN Address               : {0}'.format(
                    self.cls_nodes[key][2]))
        print('\n')
        print('Checking LUNs availability...')
        print('Please wait the finish message.\n')

        try:
            self._lun_availability(self.lu_ids)
        except ValueError, e:
            raise ValueError(e)

        print ('\nLUN availability finished.\n')

        print('Checking HLU availability...')
        print('Please wait the finish message.\n')

        try:
            self._hlu_availability(self.hlu_ids, self.stggroup_name)

            if self.cls == 'y':
                for cluster_node in self.cls_nodes.keys():
                    try:
                        self._hlu_availability(
                            self.cls_nodes[cluster_node][3],
                            self.cls_nodes[cluster_node][1])
                    except ValueError, e:
                        raise ValueError(e)
        except ValueError, e:
            raise ValueError(e)

        print ('\nHLU availability finished.\n')

    def execute(self):

        global exec_return, evidence_file_name

        # init the evidence header
        evidence_file_name = '{0}/stgadm/evidences/{1}_{2}_{3}.txt'.format(
            config.stghome, self.change, self.stggroup_name, self.time)

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

            if output_data[0] != 0:
                f_evidence_file.write(output_data[2])

            f_evidence_file.close()

        def _alternator(stg_1ip, stg_2ip):
            """ Create an class to alternate between two IPs of storage

            :param stg_1ip: First IP address
            :param stg_2ip: Second IP Address
            :return:
            """
            while True:
                yield stg_1ip
                yield stg_2ip

        evidence_file = open(evidence_file_name, 'a')
        evidence_file.write(
            "# CREATING/ALLOCATION LUN(s)\n"
            "############################\n".format(
                self.stggroup_name))
        evidence_file.close()

        ip_address = _alternator(self.stg_1ip, self.stg_2ip)

        # dev creation
        for l_id in self.lu_ids:
            exec_return = self.vnx.create_dev(ip_address.next(), self.lun_size,
                                              self.stg_pool, l_id,
                                              "{0}_LUN_{1}".format(
                                                  self.lun_sid, l_id),
                                              self.lun_type)

            _write_evidence(exec_return, evidence_file_name)
            remove_reserved_id(l_id)

        # dev mapping
        hlu_count = 0
        for l_id in self.lu_ids:
            exec_return = self.vnx.mapping_dev(self.stggroup_name,
                                               self.hlu_ids[hlu_count],
                                               l_id)
            _write_evidence(exec_return, evidence_file_name)
            remove_reserved_hlu_id(self.hlu_ids[hlu_count], self.stggroup_name)
            hlu_count += 1

        # write the status of volume group
        evidence_file = open(evidence_file_name, 'a')
        evidence_file.write("# LUN list for Storage Group {0}\n".format(
            self.stggroup_name))
        evidence_file.close()

        exec_return = self.vnx.show_stggroup(self.stggroup_name)

        _write_evidence(exec_return, evidence_file_name)

        # cluster mapping devices
        #
        # TIP: self.cluster_nodes
        #      [0] hostname client on storage
        #      [1] storage group name
        #      [2] wwn client
        #      [3] (array) with selected hlus
        if self.cls == 'y':

            evidence_file = open(evidence_file_name, 'a')
            evidence_file.write("# CLUSTER NODE (adding LUN(s))\n"
                                "##############################\n")
            evidence_file.close()

            for cluster_node in self.cls_nodes.keys():

                evidence_file = open(evidence_file_name, 'a')
                evidence_file.write(
                    "# Adding LUN(s) for Cluster node {0} "
                    "[Storage Group {1}]\n".format(
                        self.cls_nodes[cluster_node][0],
                        self.cls_nodes[cluster_node][1]))
                evidence_file.close()

                hlu_count = 0
                for l_id in self.lu_ids:
                    exec_return = self.vnx.mapping_dev(
                        self.cls_nodes[cluster_node][1],
                        self.cls_nodes[cluster_node][3][hlu_count],
                        l_id
                    )
                    _write_evidence(exec_return, evidence_file_name)
                    remove_reserved_hlu_id(
                        self.cls_nodes[cluster_node][3][hlu_count],
                        self.cls_nodes[cluster_node][1])
                    hlu_count += 1

                evidence_file = open(evidence_file_name, 'a')
                evidence_file.write(
                    "# LUN list for Storage Group {0}\n".format(
                        self.cls_nodes[cluster_node][1]))
                evidence_file.close()
                exec_return = self.vnx.show_stggroup(
                    self.cls_nodes[cluster_node][1])
                _write_evidence(exec_return, evidence_file_name)

        return evidence_file_name
