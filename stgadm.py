#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#
from stgadm.menu import main_menu

try:

    main_menu()
    ''' Import the main menu of STGAdm '''
except KeyboardInterrupt:
    print ("\n\nCtrl+C pressed! Exiting without save.\n")
