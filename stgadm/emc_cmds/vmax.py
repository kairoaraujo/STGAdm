#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# 
import subprocess
import os


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

        if self.symcli_path == '' or self.sid == '' or self.wwn == '':
            msg = 'This function require all attributes.'
            return msg

    def init_ign(self):
        """
        :return: The Initiator Group Name of the client server (WWN).
        """

        self.validate_args()

        ign_cmd = "{0}/symaccess -sid {1} -type init list -wwn {2}".format(
            self.symcli_path, self.sid, self.wwn)

        c_ign = subprocess.Popen(ign_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        ign_out = c_ign.communicate()[0]

        if 'The specified initiator was not found' in ign_out:
            return ign_out
        else:
            # spliting in lines
            ign_out = ign_out.split('\n')
            # cleaning the empty elements (filter) and removing whitespaces
            # (lstrip)
            ign_out = filter(None, ign_out)[-1].lstrip()
            return ign_out

     def init_mvn(self, ign=''):
        """
        Get the Mask View Names by Initiator Group Name
        :param ign: Initiator Group Name. check init_ign()
        :return: Mask View Name
        """

        mvn_cmd = "{0}/symaccess -sid {1} -type init show {2}".format(
            self.symcli_path, self.sid, ign)

        c_mvn = subprocess.Popen(mvn_cmd.split(), stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
        mvn_out = c_mvn.communicate()[0]

        mvn_out = mvn_out.split('Masking View Names')[1]
        mvn_out = mvn_out.split()[1].lstrip()

        return mvn_out

     def init_sgn(self, mvn=''):
         """
         Get the Storage Group Name by the Mask View Name

         :param mvn: Mask View Name check init_mvn()
         :return: Storage Group Name
         """

         sgn_cmd = '{0}/symaccess -sid {1} show view {2}'.format(
             self.symcli_path, self.sid, mvn)

         c_sgn = subprocess.Popen(sgn_cmd.split(), stdout=subprocess.PIPE,
                                  stderr=subprocess.PIPE)

         mvn_out = c_sgn.communicate()[0]

         mvn_out = mvn_out.split('Storage Group Name')
         mvn_out = mvn_out.split()[1]

         return mvn_out


