#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

# STGAdm installation directory
stghome = "/Users/kairoaraujo/Dev/stgadm"


# Storage List
# Important:
#   This require an order that is:
#   'NAME OF STORAGE':['TYPE','SID'],
#
#       TYPES available:
#       - EMC_VMAX     EMC VMAX Storages
#       - IBM_DS8K     IBM DS8K Storages
#
#       SID Configuration:
#       - EMC VMAX: Use the last three number
#       - IBM DS8K: Use the profile file. ex: dscli.profile_XYZAB51
#

storages = {
    'EMC VMAX 0168': ['EMC_VMAX', '168'],
    'IBM DS8K XYZAB51': ['IBM_DS8K', 'dscli.profile_XYZAB51']
}

# EMC Configurations
#
# SYMCLI bin dir path
symcli_path = "/opt/emc/SYMCLI/bin/"
lspool_args = '-gb -thin'

# IBM Configurations
#
# DSCLI binary
dscli_bin = "/opt/ibm/dscli/dscli"
# DSCLI profiles path
dscli_profile_path = "/opt/ibm/dscli/profile/"
