#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#

# STGAdm installation directory
stghome = "/Users/kairoaraujo/Documents/Dev/Python/stgadm"

# Storage List
# Important:
#   This require an order that is:
#   'NAME OF STORAGE':['TYPE','SID'],
#
#       Types available:
#       - EMC_VMAX     EMC VMAX Storages
#       - EMC_VX       EMC VX Storages
#       - IBM_DS8K     IBM DS8K Storages

storages = {
    '0002':['EMC_VMAX','002'],
    '0168':['EMC_VMAX','168'],
    '0314 [Cloud Computing)':['EMC_VX','314'],
    'CD01 (IBM pSeries)':['IBM_DS8K','CD01']
}


symcli_path = "echo /opt/emc/SYMCLI/bin/"


modeop = 'demo'