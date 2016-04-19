#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

# STGAdm installation directory
stghome = "/opt/STGAdm"


# Storage List
# Important:
#   This require an order that is:
#   'NAME OF STORAGE':['TYPE','CONFIG'],
#
#       TYPES available:
#       - EMC_VMAX     EMC VMAX Storages
#       - EMC_VNX      EMC VNX Storages
#       - IBM_DS8K     IBM DS8K Storages
#
#       SID Configuration:
#       - EMC VMAX: Use the last three number
#       - EMC VNX : Use the primary IP, secondary IP, user, password and scope
#       - IBM DS8K: Use the profile file. ex: dscli.profile_XYZAB51
#

storages = {
    'EMC VMAX 168': ['EMC_VMAX', '168'],
    'EMC VNX  199': ['EMC_VNX', '10.44.2.199', '10.44.2.200', 'admin', 'password', '0'],
    'IBM DS8K B51': ['IBM_DS8K', 'dscli.profile_XYZAB51']
}

# EMC Configurations
# ------------------
#
# [VMAX]
#
# SYMCLI bin dir path
symcli_path = "/opt/emc/SYMCLI/bin/"
lspool_args = '-gb -thin'

# [VNX]
#
# NAVISECCLI
naviseccli_bin = '/opt/Navisphere/bin/naviseccli'
# LUN Type used to create
lun_type_create = 'NonThin'

# IBM Configurations
# ------------------
#
# [DS8K]
#
# DSCLI binary
dscli_bin = "/opt/ibm/dscli/dscli"
# DSCLI profiles path
dscli_profile_path = "/opt/ibm/dscli/profile/"
