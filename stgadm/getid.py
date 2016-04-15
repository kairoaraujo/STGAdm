#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
import config
import pystorage
import subprocess
import os


class DS8K:
    def __init__(self, dscli_bin, dscli_profile_path, lss_id):
        """
        Manage the IDs for IBM DS8K

        :param dscli_bin: path of dscli_bin
        :param dscli_profile_path: profile file os dscli
        :param lss_id: LSS ID tat you want to ge the free ids (ex: A6)
        :return:
        """

        self.dscli_bin = dscli_bin
        self.dscli_profile_path = dscli_profile_path
        self.lss_id = lss_id

        # test lss_id
        if len(self.lss_id) != 2:
            raise ValueError('lss_id need to have 2 valid characters in hex.\n'
                             'Tip: Between 00 and FF.')

        try:
            int(self.lss_id, 16)
        except:
            raise ValueError(
                'lss_id need to be a string with valid hex value.\n'
                'Tip: Between 00 and FF.')

    def _check_lss(self, lss_list_used, lss_list_reserved):

        code_cmd = 'sh {0}/tools/hexcount.sh {1}00 {1}FF'.format(
            config.stghome, self.lss_id)
        hexa = subprocess.Popen(code_cmd.split(),
                                stderr=subprocess.PIPE,
                                stdout=subprocess.PIPE)
        hexa_out, hexa_err = hexa.communicate()

        if hexa.returncode != 0:
            raise EnvironmentError('ERROR: {0}'.format(hexa_err))

        else:
            lss_list_full = []
            for l_hexa in hexa_out.split('\n'):
                if l_hexa != '':
                    lss_list_full.append(l_hexa)

        for l_reserved in lss_list_reserved:
            lss_list_used.append(l_reserved.split('\n')[0])

        lss_list_free = list(set(lss_list_full) - set(lss_list_used))

        return sorted(lss_list_free)

    def free_lss(self):
        """

        :return: array with free ids (lss ID) from DS8K
        """

        lss_list_used = []
        lss_list_reserved = []
        ds8k = pystorage.DS8K(self.dscli_bin, self.dscli_profile_path)
        lss_list = ds8k.lsfbvol('-lss {0}'.format(self.lss_id))
        if lss_list[0] != 0:
            print ("ERROR: {0}".format(lss_list[1]))

        for l_lss in lss_list[1].split('\n')[3:]:
            try:
                lss_list_used.append(l_lss.split()[1])
            except IndexError:
                pass

        if os.path.isfile(
                '{0}/stgadm/data/reserved_ids.db'.format(config.stghome)):
            lss_reserved_file = open('{0}/stgadm/data/reserved_ids.db'.format(
                config.stghome
            ), 'r')

            for l_lss in lss_reserved_file.readlines():
                if l_lss.startswith('{0}'.format(self.lss_id)[0:2]):
                    lss_list_reserved.append(l_lss)

        return self._check_lss(lss_list_used, lss_list_reserved)


class VNX:
    def __init__(self, naviseccli_bin, ip, stg_user, stg_pass, stg_scope,
                 stg_pool):
        """
        Manage the IDs for EMC VNX

        :param naviseccli_bin: full path of naviseccli binary
        :param ip: IP of storage
        :param stg_user: user for storage
        :param stg_pass: password user for storage
        :param stg_scope: scope to be used (0 is default)
        :param stg_pool: Storage pool to get the free IDs

        """

        self.naviseccli_bin = naviseccli_bin
        self.ip = ip
        self.stg_user = stg_user
        self.stg_pass = stg_pass
        self.stg_scope = stg_scope
        self.stg_pool = stg_pool

    def free_lu(self):
        """

        :return: array with free ids (lu) from EMC VNX.
        """

        vnx = pystorage.EMC.VNX(self.naviseccli_bin, self.ip, self.ip,
                                self.stg_user, self.stg_pass, self.stg_scope)

        used_lu = vnx.get_luns(self.stg_pool)

        if used_lu[0] != 0:
            exit()
        else:
            used_lu = used_lu[1]

        if os.path.isfile(
                '{0}/stgadm/data/vnx_reserved_ids.db'.format(config.stghome)):
            lu_reserv_file = open('{0}/stgadm/data/vnx_reserved_ids.db'.format(
                config.stghome
            ), 'r')

            for l_lu in lu_reserv_file.readlines():
                used_lu.append(l_lu)

        used_lu.sort(key=int)
        used_lu = map(int, used_lu)

        # create the free lu possible (default 8191)
        full_lu = range(8191)

        free_lu = list(set(full_lu) - set(used_lu))

        return free_lu

    def free_hlu(self, stggroup_name):
        """

        :param stggroup_name: Storage Group Name
        :return: array with free hlu ids (hlu) from EMC VNX.
        """

        vnx = pystorage.EMC.VNX(self.naviseccli_bin, self.ip, self.ip,
                                self.stg_user, self.stg_pass, self.stg_scope)

        used_hlu = vnx.get_hlu_stggroup(stggroup_name)

        if used_hlu[0] != 0:
            exit()
        else:
            used_hlu = used_hlu[1]

        if os.path.isfile(
                '{0}/stgadm/data/vnx_reserved_hlu_{1}.db'.format(
                    config.stghome, stggroup_name)):
            lu_reserv_file = open(
                '{0}/stgadm/data/vnx_reserved_hlu_{1}.db'.format(
                    config.stghome, stggroup_name
                ), 'r')

            for l_hlu in lu_reserv_file.readlines():
                used_hlu.append(l_hlu)

        used_hlu.sort(key=int)
        used_hlu = map(int, used_hlu)

        # create the free hlu possible (default 256)
        full_hlu = range(256)

        free_hlu = list(set(full_hlu) - set(used_hlu))

        return free_hlu
