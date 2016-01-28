#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

# STGAdm installation directory
stghome = "/opt/Atividades/kairo/STGAdm-master"
# stghome = "/Users/kairoaraujo/Dev/stgadm"

# Storage List
# Important:
#   This require an order that is:
#   'NAME OF STORAGE':['TYPE','SID'],
#
#       Types available:
#       - EMC_VMAX     EMC VMAX Storages
#       - EMC_VNX      EMC VNX Storages
#       - IBM_DS8K     IBM DS8K Storages

storages = {
    '0002': ['EMC_VMAX', '002'],
    '0168': ['EMC_VMAX', '168'],
    '0314 [Cloud Computing]': ['EMC_VNX', '314'],
    'CD01 (IBM pSeries)': ['IBM_DS8K', 'CD01']
}

# EMC Configurations
#

# SYMCLI bin dir path
symcli_path = "/opt/emc/SYMCLI/bin/"

# IBM Configurations
#

# DSCLI binary
dscli_bin = "/opt/ibm/dscli/dscli"
# DSCLI profiles path
dscli_profile_path = "/opt/ibm/dscli/profile/"
