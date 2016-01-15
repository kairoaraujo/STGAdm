#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
import subprocess


class VMAX(object):
    """ Class VMAX works with EMC VMAX Storage """

    def __init__(self, symcli_path='', sid='', wwn=''):
        """
        :param symcli_path: Path installation of SYMCLI
        :param sid: Storage SID
        :param wwn: WWN of the client server
        """

        self.symcli_path = symcli_path
        self.sid = sid
        self.wwn = wwn

    def __repr__(self):
        """
        :return: representation (<VMAX>).
        """

        representation = '<VMAX>'
        return representation

    def validate_args(self):
        """ Validate if the required args is declarated. """

        if self.symcli_path == '' or self.sid == '':
            msg = 'This function require all attributes.'
            return msg

    def lspools(self, args=''):
        """ List of pools """

        self.validate_args()

        lspools_cmd = '{0}/symcfg -sid {1} list -pool {2}'.format(
            self.symcli_path, self.sid, args)

        c_lspools = subprocess.Popen(lspools_cmd.split(),
                                     stdout=subprocess.PIPE,
                                     stderr=subprocess.PIPE)

        lspool_out, lspool_err = c_lspools.communicate()

        if c_lspools.returncode == 0:
            lspool_out = lspool_out.split('Legend:')
            lspool_out = lspool_out[1] # first part only
            return c_lspools.returncode, lspool_out
        else:
            return c_lspools.returncode, lspool_err

    def get_ign(self, wwn=''):
        """
        :return: The Initiator Group Name of the client server (WWN).
        """

        self.validate_args()

        ign_cmd = "{0}/symaccess -sid {1} -type init list -wwn {2}".format(
            self.symcli_path, self.sid, wwn)

        c_ign = subprocess.Popen(ign_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        ign_out, ign_err = c_ign.communicate()

        if c_ign.returncode == 0:
            # spliting in lines
            ign_out = ign_out.split('\n')
            # cleaning the empty elements (filter) and removing whitespaces
            # (lstrip)
            ign_out = filter(None, ign_out)[-1].lstrip()
            return c_ign.returncode, ign_out

        else:
            return c_ign.returncode, ign_err

    def get_mvn(self, ign=''):
        """
        Get the Mask View Names by Initiator Group Name
        :param ign: Initiator Group Name. check init_ign()
        :return: Mask View Name
        """

        mvn_cmd = "{0}/symaccess -sid {1} -type init show {2}".format(
            self.symcli_path, self.sid, ign)

        c_mvn = subprocess.Popen(mvn_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        mvn_out, mvn_err = c_mvn.communicate()

        if c_mvn.returncode == 0:
            mvn_out = mvn_out.split('Masking View Names')[1]
            mvn_out = mvn_out.split()[1].lstrip()

            return c_mvn.returncode, mvn_out

        else:
            return c_mvn.returncode, mvn_err

    def get_sgn(self, mvn=''):
        """
         Get the Storage Group Name by the Mask View Name

         :param mvn: Mask View Name check init_mvn()
         :return: Storage Group Name
         """

        sgn_cmd = '{0}/symaccess -sid {1} show view {2}'.format(
            self.symcli_path, self.sid, mvn)

        c_sgn = subprocess.Popen(sgn_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)

        sgn_out, sgn_err = c_sgn.communicate()

        if c_sgn.returncode == 0:
            sgn_out = sgn_out.split('Storage Group Name ')[1]
            sgn_out = sgn_out.split()[1]

            return c_sgn.returncode, sgn_out
        else:
            return c_sgn.returncode, sgn_err
