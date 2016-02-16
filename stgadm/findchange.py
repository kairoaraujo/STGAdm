#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Imports
##########################################################################
import os
import fnmatch
import config


def select():
    """ Select the change/ticket file. """
    print ("\n[Change/Ticket/WO Execution]\n"
           "\nSelect the Change/Ticket/WO to execute:\n")
    listchanges = fnmatch.filter(
        os.listdir("{0}/stgadm/changes/".format(config.stghome)), "change*.py")
    listchanges_length = len(listchanges) - 1
    if listchanges_length == -1:
        print ('No changes found. Exiting\n')
        exit()
    count = 0
    while count <= listchanges_length:
        print ("{0} : {1}".format(count, listchanges[count]))
        count += 1
    change_exec = None
    while True:
        try:
            change_option = int(
                raw_input("\nWhat's change/ticket id you want execute?: "))
            change_exec = (listchanges[change_option])
            break
        except (IndexError, ValueError):
            print(
                '\tERROR: Select an existing option between 0 and {0}.'.format(
                    listchanges_length))

    return change_exec


def ls():
    """ Return the list of changes/tickets file available or None
     if don't exist files
    """
    listchanges = fnmatch.filter(
        os.listdir("{0}/stgadm/changes/".format(config.stghome)), "*.py")
    listchanges_length = len(listchanges) - 1
    if listchanges_length == -1:
        return None
    else:
        return listchanges
