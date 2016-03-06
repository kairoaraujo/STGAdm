STGAdm - Storage Admin Tool
===========================

This is a util to use for Storage Disk Administration.

Support IBM DS8000 (DS8K) and EMC VMAX. (check Version for more informations)


Version
-------

-  0.3-beta

   - Added support for cluster provisioning on IBM DS8K

-  0.2-beta

   - Working for add new devices for existent host client on IBM DS8K

-  0.1-beta

   - Working for add new devices for existent host client on EMC VMAX (1 & 2)
   - Initial release

    
Installation / Configuration / Using
------------------------------------

- Requirement

    $ pip install PyStorage

- Download latest version of STGAdm

    https://github.com/kairoaraujo/STGAdm/releases
 
Uncompress the util

- Configure the STGAdm

    STGAdm/stgadm/config.py

- Execute the STGAdm

    $ python stgadm.py

An interactive menu will be appear. Have fun!

Screenshots
-----------

- Creating the change/ticket/wo

.. image:: images/ss1.png

.. image:: images/ss-ds8k-1.png

.. image:: images/ss-ds8k-2.png
    
.. image:: images/ss-ds8k-3.png


- Executing the change/ticket/wo

.. image:: images/ss-ds8k-4.png

.. image:: images/ss-ds8k-5.png

.. image:: images/ss-ds8k-6.png