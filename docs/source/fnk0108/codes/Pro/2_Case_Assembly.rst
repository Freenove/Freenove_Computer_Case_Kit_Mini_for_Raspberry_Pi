##############################################################################
Chapter 2 Case Assembly
##############################################################################

It is recommended to assemble and use the Freenove Computer Case Kit Mini for Raspberry Pi according to this tutorial. Otherwise, it may lead to incorrect device installation or damage. Please check all the parts again. Before getting started, please check the part list. If any component is missing from your kit, do not start assembly; instead, please email our support team at support@freenove.com to get the missing parts.

**Ensure the device is powered off before assembly.**

Use of the Screwdriver Bit Holder
*********************************************

.. table::
    :class: table-line
    :align: center
    
    +-----------------------------------------------------------------------------------------------+
    | When installing the brass standoff, simply place it directly into the bit holder.             |
    |                                                                                               |
    | |Chapter02_44|                                                                                |
    +-----------------------------------------------------------------------------------------------+
    | When installing the M3.7x10 Countersunk Head Screws, please use the PH2 hexagonal cross-bit.  |
    |                                                                                               |
    | |Chapter02_45|                                                                                |
    +-----------------------------------------------------------------------------------------------+
    | When installing other screws, please use the PH0 hexagonal cross-bit.                         |
    |                                                                                               |
    | |Chapter02_46|                                                                                |
    +-----------------------------------------------------------------------------------------------+

.. |Chapter02_44| image:: ../_static/imgs/2_Case_Assembly/Chapter02_44.png
.. |Chapter02_45| image:: ../_static/imgs/2_Case_Assembly/Chapter02_45.png
.. |Chapter02_46| image:: ../_static/imgs/2_Case_Assembly/Chapter02_46.png

2.1 Raspberry Pi Assembly
*********************************

2.1.1 Installing Standoffs
===================================

.. table::
    :class: table-line
    :align: center
    
    +-----------------------------------------------------------------------------------------+
    | Step 1: Install M2.5*10+4 Brass Standoffs and M2.5*7 Brass Standoffs onto the RPi 5.    |
    |                                                                                         |
    | |Chapter02_47|                                                                          |
    +-----------------------------------------------------------------------------------------+
    | Step 2: Secure the M2.5*7 Brass Standoff onto the RPi 5 with M2.5x4x5 flat-head screws. |
    |                                                                                         |
    | |Chapter02_48|                                                                          |
    +-----------------------------------------------------------------------------------------+

.. |Chapter02_47| image:: ../_static/imgs/2_Case_Assembly/Chapter02_47.png
.. |Chapter02_48| image:: ../_static/imgs/2_Case_Assembly/Chapter02_48.png

2.1.2 Connecting CAM/DIS Cable and Installing the Tower Cooler 
========================================================================

.. table::
    :class: table-line
    :align: center
    
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | :red:`Note: Installing a tower cooler may obstruct access to the CAM/DISP interface. If you need to connect a device (such as a camera) to this interface, you must connect the cable before installing the cooler. Otherwise, you may skip this step.` |
    |                                                                                                                                                                                                                                                         |
    | |Chapter02_49|                                                                                                                                                                                                                                          |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Connect the 12cm SH1.0mm 4-pin cable to the FAN (J17) interface on the RPi 5. (:red:`This is a non-reversible connector. Improper handling or misalignment during connection will result in permanent damage to the interface.`)                |
    |                                                                                                                                                                                                                                                         |
    | |Chapter02_50|                                                                                                                                                                                                                                          |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Identify the five thermal pads by size and apply each one to its corresponding chip on the RPi 5. (:red:`Important: Ensure you remove the protective film from both sides of each pad to guarantee optimal thermal conductivity.`)              |
    |                                                                                                                                                                                                                                                         |
    | |Chapter02_51|                                                                                                                                                                                                                                          |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Steps 3: Fix the Tower Cooler to RPi 5 with the Nylon standoffs.                                                                                                                                                                                        |
    |                                                                                                                                                                                                                                                         |
    | |Chapter02_52|                                                                                                                                                                                                                                          |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_49| image:: ../_static/imgs/2_Case_Assembly/Chapter02_49.png
.. |Chapter02_50| image:: ../_static/imgs/2_Case_Assembly/Chapter02_50.png
.. |Chapter02_51| image:: ../_static/imgs/2_Case_Assembly/Chapter02_51.png
.. |Chapter02_52| image:: ../_static/imgs/2_Case_Assembly/Chapter02_52.png

2.2 Mounting GPIO/Switch/NVMe/Power Board
*************************************************

2.2.1 Assembling GPIO Board and Switch Board
================================================

.. table::
    :class: table-line
    :align: center
    
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Before installing the GPIO Board, ensure that its connector is properly aligned with the Raspberry Pi 5's GPIO header. Once aligned, press it down evenly and firmly. (:red:`Note: Correct pin alignment is essential. Misalignment can cause a short circuit and damage the Raspberry Pi.`)             |
    |                                                                                                                                                                                                                                                                                                                  |
    | |Chapter02_53|                                                                                                                                                                                                                                                                                                   |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Connect the SH1.0mm_2P Same-Direction Cable (5cm) and the SH1.0mm_3P Same-Direction Cable (5cm) to the RTC and UART headers on the Raspberry Pi 5 before installing the Switch Board, **as the Switch Board will block access to the RTC header once installed.**                                        |
    |                                                                                                                                                                                                                                                                                                                  |
    | |Chapter02_54|                                                                                                                                                                                                                                                                                                   |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Align the pogo pins on the Switch Board with the two vias located between the Raspberry Pi's Type-C and HDMI0 ports. Once properly positioned, secure it using an M2.5x4x5 flat-head screw.                                                                                                              |
    |                                                                                                                                                                                                                                                                                                                  |
    | |Chapter02_55|                                                                                                                                                                                                                                                                                                   |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 4: Connect SD Card to 0.5mm-16P FPC cable. Insert the "**To Pi**" end into the **SD card slot** on the RPi 5, and insert the "**To Adapter**" end into the "**SD Card In**" interface on the GPIO Board.                                                                                                    |
    |                                                                                                                                                                                                                                                                                                                  |
    | (:red:`Gently flip-up the clip on the SD card interface to insert the cable.`)                                                                                                                                                                                                                                   |
    |                                                                                                                                                                                                                                                                                                                  |
    | |Chapter02_56|                                                                                                                                                                                                                                                                                                   |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 5: Connect the other end of the 12cm SH1.0mm 4-pin cable to the PI FAN IN header on the GPIO Board. (:red;`This is a non-reversible connector. Improper handling or misalignment during connection will result in permanent damage to the interface.`)                                                      |
    |                                                                                                                                                                                                                                                                                                                  |
    | |Chapter02_57|                                                                                                                                                                                                                                                                                                   |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 6: Connect the tower coller to the **FAN1** header on the GPIO board. (:red:`Note: Speed feedback is only available when a fan is connected to the FAN1 header. This is a non-reversible connector. Improper handling or misalignment during connection will result in permanent damage to the interface.`) |
    |                                                                                                                                                                                                                                                                                                                  |
    | |Chapter02_58|                                                                                                                                                                                                                                                                                                   |
    +------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_53| image:: ../_static/imgs/2_Case_Assembly/Chapter02_53.png
.. |Chapter02_54| image:: ../_static/imgs/2_Case_Assembly/Chapter02_54.png
.. |Chapter02_55| image:: ../_static/imgs/2_Case_Assembly/Chapter02_55.png
.. |Chapter02_56| image:: ../_static/imgs/2_Case_Assembly/Chapter02_56.png
.. |Chapter02_57| image:: ../_static/imgs/2_Case_Assembly/Chapter02_57.png
.. |Chapter02_58| image:: ../_static/imgs/2_Case_Assembly/Chapter02_58.png

2.2.2 Installing the Power Board
==============================================

.. table::
    :class: table-line
    :align: center
    
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Insert one end of the 86mm HDMI FPC Cable into the FPC interface on thePower Board.                                                                                                 |
    |                                                                                                                                                                                             |
    | |Chapter02_59|                                                                                                                                                                              |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Connect the other ends of the SH1.0mm_2P Same-Direction Cable (5cm) and the SH1.0mm_3P Same-Direction Cable (5cm) to the **RTC and UART headers** on the Power Board, respectively. |
    |                                                                                                                                                                                             |
    | |Chapter02_60|                                                                                                                                                                              |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Align the Power Board with the Raspberry Pi 5's Type-C, HDMI0, and HDMI1 ports, then insert the Power Board.                                                                        |
    |                                                                                                                                                                                             |
    | |Chapter02_61|                                                                                                                                                                              |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_59| image:: ../_static/imgs/2_Case_Assembly/Chapter02_59.png
.. |Chapter02_60| image:: ../_static/imgs/2_Case_Assembly/Chapter02_60.png
.. |Chapter02_61| image:: ../_static/imgs/2_Case_Assembly/Chapter02_61.png

2.2.3 Assembling the NVMe Adapter Board
==============================================

Please select your product model below to view the corresponding installation instructions for the NVMe Adapter Board.

For **FNK0108P/U**: :ref:`NVMe Adapter Board <fnk0108/codes/pro/2_case_assembly:installing nvme adapter board>`

For **FNK0108Q/V**: :ref:`Dual-NVMe Adapter Board <fnk0108/codes/pro/2_case_assembly:installing dual-nvme adapter board>`

For **FNK0108R/W**: :ref:`Quad-NVMe Adapter Board <fnk0108/codes/pro/2_case_assembly:installing quad-nvme adapter board>`

Installing NVMe Adapter Board
----------------------------------------------

.. table::
    :class: table-line
    :align: center
    
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Based on the physical dimensions of your SSD, install the M2.5x3+3 brass standoff into the mounting hole corresponding to the 2230/2242/2260/2280 specification. Secure it from the reverse side using an M2.5 nut.                                                                                               |
    |                                                                                                                                                                                                                                                                                                                           |
    | |Chapter02_62|                                                                                                                                                                                                                                                                                                            |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Tilt the SSD to insert it into the NVMe slot, and then secure it using an M2.5x2.5x5 flat-head screw.                                                                                                                                                                                                             |
    |                                                                                                                                                                                                                                                                                                                           |
    | |Chapter02_63|                                                                                                                                                                                                                                                                                                            |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Align the NVMe Adapter Board with the mounting holes on the GPIO Board and secure it with M2.5x4x5 flat-head screws.                                                                                                                                                                                              |
    |                                                                                                                                                                                                                                                                                                                           |
    | |Chapter02_64|                                                                                                                                                                                                                                                                                                            |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 4: Connect the PCIe FPC cable. Connect the **To Pi** end to the RPi 5's **PCIe interface**, and the **To Adapter** end to the NVMe Adapter hat’s **FPC interface**. (:red:`Caution: Gently pull the FPC latch to prevent damage that may cause FPC cable connection failure. Pay attention to the cable direction.`) |
    |                                                                                                                                                                                                                                                                                                                           |
    | |Chapter02_65|                                                                                                                                                                                                                                                                                                            |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_62| image:: ../_static/imgs/2_Case_Assembly/Chapter02_62.png
.. |Chapter02_63| image:: ../_static/imgs/2_Case_Assembly/Chapter02_63.png
.. |Chapter02_64| image:: ../_static/imgs/2_Case_Assembly/Chapter02_64.png
.. |Chapter02_65| image:: ../_static/imgs/2_Case_Assembly/Chapter02_65.png

Installing Dual-NVMe Adapter Board
-----------------------------------------------

.. table::
    :class: table-line
    :align: center
    
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Based on the physical dimensions of your SSD, install two M2.5x3+3 brass standoffs into the mounting hole corresponding to the 2230/2242/2260/2280 specification. Secure them from the reverse side with M2.5 nuts.                                                                                                                     |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_66|                                                                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | :red:`Note: This Adapter Board supports up to two SSDs. Install 0 to 2 SSDs based on your preference.`                                                                                                                                                                                                                                          |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | Step 2: Tilt the SSDs to inster them into the two NVMe slots, and then secure them using M2.5x2.5x5 flat-head screws.                                                                                                                                                                                                                           |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_67|                                                                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Align the Dual-NVMe Adapter Board with the mounting holes on the GPIO Board and secure it with M2.5x4x5 flat-head screws.                                                                                                                                                                                                               |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_68|                                                                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 4: Connect the PCIe FPC cable. Connect the **To Pi** end to the RPi 5's **PCIe interface**, and the **To Adapter** end to the NVMe Adapter hat's **FPC interface**.(:red:`Caution: Gently pull the FPC latch to prevent damage that may cause FPC cable connection failure. Pay attention to the cable direction.`)                        |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_69|                                                                                                                                                                                                                                                                                                                                  |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_70|                                                                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 5: Connect two female-to-female jumper wires. Attach one end to the **pin headers** on the Dual-NVMe Adapter Board, and the other end to the **5V PWR** on the GPIO Board. (:red:`Caution: The red wire must connect to the 5V pin, and the black wire to the GND pin. Incorrect wiring may cause a short circuit and damage the device.`) |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_71|                                                                                                                                                                                                                                                                                                                                  |
    |                                                                                                                                                                                                                                                                                                                                                 |
    | **Generally, connecting the two jumper wires is not required. However, for SSDs with higher power consumption, it is necessary to connect them to ensure adequate power supply and stable operation.**                                                                                                                                          |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_66| image:: ../_static/imgs/2_Case_Assembly/Chapter02_66.png
.. |Chapter02_67| image:: ../_static/imgs/2_Case_Assembly/Chapter02_67.png
.. |Chapter02_68| image:: ../_static/imgs/2_Case_Assembly/Chapter02_68.png
.. |Chapter02_69| image:: ../_static/imgs/2_Case_Assembly/Chapter02_69.png
.. |Chapter02_70| image:: ../_static/imgs/2_Case_Assembly/Chapter02_70.png
.. |Chapter02_71| image:: ../_static/imgs/2_Case_Assembly/Chapter02_71.png

Installing Quad-NVMe Adapter Board
--------------------------------------------

.. table::
    :class: table-line
    :align: center
    
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Based on the physical dimensions of your SSD, install four M2.5x3+3 brass standoffs into the mounting hole corresponding to the 2230/2242/2260/2280 specification. Secure them from the reverse side with M2.5 nuts. It is recommended that you install standoffs to all the four mounting holes.                               |
    |                                                                                                                                                                                                                                                                                                                                         |
    | |Chapter02_72|                                                                                                                                                                                                                                                                                                                          |
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | :red:`Note: This Adapter Board supports up to four SSDs. Install 0 to 4 SSDs based on your preference.`                                                                                                                                                                                                                                 |
    |                                                                                                                                                                                                                                                                                                                                         |
    | Step 2: Tilt the SSDs to inster them into the two NVMe slots on the front side, and then secure them using M2.5x2.5x5 flat-head screws.                                                                                                                                                                                                 |
    |                                                                                                                                                                                                                                                                                                                                         |
    | |Chapter02_73|                                                                                                                                                                                                                                                                                                                          |
    |                                                                                                                                                                                                                                                                                                                                         |
    | Step 3: Tilt the SSDs to inster them into the two NVMe slots on the back side, and secure them using M2.5x2.5x5 flat-head screws.                                                                                                                                                                                                       |
    |                                                                                                                                                                                                                                                                                                                                         |
    | |Chapter02_74|                                                                                                                                                                                                                                                                                                                          |
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 4: Align the Quad-NVMe Adapter Board with the mounting holes on the GPIO Board and secure it with M2.5x4x5 flat-head screws.                                                                                                                                                                                                       |
    |                                                                                                                                                                                                                                                                                                                                         |
    | |Chapter02_75|                                                                                                                                                                                                                                                                                                                          |
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 5: Connect the PCIe FPC cable. Connect the **To Pi** end to the RPi 5's **PCIe interface**, and the To **Adapter** end to the NVMe Adapter hat's **FPC interface**.(:red:`Caution: Gently pull the FPC latch to prevent damage that may cause FPC cable connection failure. Pay attention to the cable direction.`)                |
    |                                                                                                                                                                                                                                                                                                                                         |
    | |Chapter02_76|                                                                                                                                                                                                                                                                                                                          |
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 6: Connect two female-to-female jumper wires. Attach one end to the pin headers on the Quad-NVMe Adapter Board, and the other end to the 5V PWR on the GPIO Board. (:red:`Caution: The red wire must connect to the 5V pin, and the black wire to the GND pin. Incorrect wiring may cause a short circuit and damage the device.`) |
    |                                                                                                                                                                                                                                                                                                                                         |
    | |Chapter02_77|                                                                                                                                                                                                                                                                                                                          |
    |                                                                                                                                                                                                                                                                                                                                         |
    | **Generally, connecting the two jumper wires is not required. However, for SSDs with higher power consumption, it is necessary to connect them to ensure adequate power supply and stable operation.**                                                                                                                                  |
    +-----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_72| image:: ../_static/imgs/2_Case_Assembly/Chapter02_72.png
.. |Chapter02_73| image:: ../_static/imgs/2_Case_Assembly/Chapter02_73.png
.. |Chapter02_74| image:: ../_static/imgs/2_Case_Assembly/Chapter02_74.png
.. |Chapter02_75| image:: ../_static/imgs/2_Case_Assembly/Chapter02_75.png
.. |Chapter02_76| image:: ../_static/imgs/2_Case_Assembly/Chapter02_76.png
.. |Chapter02_77| image:: ../_static/imgs/2_Case_Assembly/Chapter02_77.png

2.3 Case Assembly
****************************

2.3.1 Assembling the Power Button and Connecting its cables
====================================================================

.. table::
    :class: table-line
    :align: center
    
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1:  Insert the Black Sealing Gasket into the 12mm LED Power Button.                                                                                                                                                                                                                        |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_78|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Place the assembled 12mm LED Power Button into the circular slot on the top of the case. Secure it from the inside of the case using an M12 nut.                                                                                                                                        |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_79|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Connect the 7mm SH1.0mm to quick-disconnect terminal cable (red/black) and 7mm 1.25mm to 2.8mm quick-disconnect terminal cable (yellow-yellow) to the power headers.(:red;`Note: The red wire connects to the switch's '+' terminal, and the black wire connects to the '-' terminal.`) |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_80|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_78| image:: ../_static/imgs/2_Case_Assembly/Chapter02_78.png
.. |Chapter02_79| image:: ../_static/imgs/2_Case_Assembly/Chapter02_79.png
.. |Chapter02_80| image:: ../_static/imgs/2_Case_Assembly/Chapter02_80.png

2.3.2 Installing Dust Filter, Fans, and Speakers
====================================================================

.. table::
    :class: table-line
    :align: center
    
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Peel off the protective film from the air inlet dust filter and affix it to the air inlet on the case.                                                                                                                                                                   |
    |                                                                                                                                                                                                                                                                                  |
    | |Chapter02_81|                                                                                                                                                                                                                                                                   |
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2:                                                                                                                                                                                                                                                                          |
    |                                                                                                                                                                                                                                                                                  |
    | :red:`Airflow Direction Description:`                                                                                                                                                                                                                                            |
    |                                                                                                                                                                                                                                                                                  |
    | :red:`The full fan blades are visible, is the` :combo:`red font-bolder:air intake.`                                                                                                                                                                                              |
    |                                                                                                                                                                                                                                                                                  |
    | :red:`The side with the motor frame and protective grille is the` :combo:`red font-bolder:air outlet.`                                                                                                                                                                           |
    |                                                                                                                                                                                                                                                                                  |
    | |Chapter02_82|                                                                                                                                                                                                                                                                   |
    |                                                                                                                                                                                                                                                                                  |
    | Place the dust filter between the fan and the case. Secure the fan using four M3.7x10 countersunk head screws from the outside of the case. (:red:`Note: During installation, ensure the fan's airflow direction is correct, The red arrow indicates the direction of airflow.`) |
    |                                                                                                                                                                                                                                                                                  |
    | |Chapter02_83|                                                                                                                                                                                                                                                                   |
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Remove the white protective film from the speaker and the speaker's acrylic pad.                                                                                                                                                                                         |
    |                                                                                                                                                                                                                                                                                  |
    | |Chapter02_84|                                                                                                                                                                                                                                                                   |
    |                                                                                                                                                                                                                                                                                  |
    | Align the speaker acrylic pad with the speaker and attach them together.                                                                                                                                                                                                         |
    |                                                                                                                                                                                                                                                                                  |
    | |Chapter02_85|                                                                                                                                                                                                                                                                   |
    |                                                                                                                                                                                                                                                                                  |
    | Mount the two speakers to the case frame with M2*6 Countersunk Head Screws.                                                                                                                                                                                                      |
    |                                                                                                                                                                                                                                                                                  |
    | |Chapter02_86|                                                                                                                                                                                                                                                                   |
    +----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_81| image:: ../_static/imgs/2_Case_Assembly/Chapter02_81.png
.. |Chapter02_82| image:: ../_static/imgs/2_Case_Assembly/Chapter02_82.png
.. |Chapter02_83| image:: ../_static/imgs/2_Case_Assembly/Chapter02_83.png
.. |Chapter02_84| image:: ../_static/imgs/2_Case_Assembly/Chapter02_84.png
.. |Chapter02_85| image:: ../_static/imgs/2_Case_Assembly/Chapter02_85.png
.. |Chapter02_86| image:: ../_static/imgs/2_Case_Assembly/Chapter02_86.png

2.3.3 Placing the RPi into the Case
==========================================

.. table::
    :class: table-line
    :align: center
    
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Connect the other end of the 7mm SH1.0mm to quick-disconnect terminal cable (red/black)into the **SW LED** header on the GPIO board. (:red:`This is a non-reversible connector. Improper handling or misalignment during connection will result in permanent damage to the interface.`) |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_87|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Connect the other end of the 7mm 1.25mm to 2.8mm quick-disconnect terminal cable (yellow-yellow) into the Power Board. (This is a non-reversible connector. Improper handling or misalignment during connection will result in permanent damage to the interface.)                      |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_88|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Connect the case fan to the GPIO board's **FAN2** header. (:red:`This is a non-reversible connector. Improper handling or misalignment during connection will result in permanent damage to the interface.`)                                                                            |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_89|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 4: Slide the Raspberry Pi into the case, align it with the pre-installed standoffs at the bottom, and secure it from the underside of the case with M2.5x4 countersunk head screws.                                                                                                        |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_90|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 5: Secure the NVMe Adapter board with M2.5x4x5 flat-head screws.                                                                                                                                                                                                                           |
    |                                                                                                                                                                                                                                                                                                 |
    | |Chapter02_91|                                                                                                                                                                                                                                                                                  |
    +-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_87| image:: ../_static/imgs/2_Case_Assembly/Chapter02_87.png
.. |Chapter02_88| image:: ../_static/imgs/2_Case_Assembly/Chapter02_88.png
.. |Chapter02_89| image:: ../_static/imgs/2_Case_Assembly/Chapter02_89.png
.. |Chapter02_90| image:: ../_static/imgs/2_Case_Assembly/Chapter02_90.png
.. |Chapter02_91| image:: ../_static/imgs/2_Case_Assembly/Chapter02_91.png

2.3.4 Assembling the Audio-Video Board
==================================================

.. table::
    :class: table-line
    :align: center
    
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Secure the M2.5*7 Brass Standoffs onto the Audio-Video Board with M2.5x4x5 flat-head screws.                                                          |
    |                                                                                                                                                               |
    | |Chapter02_92|                                                                                                                                                |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Align the Audio-Video Board with the pre-installed standoffs at the top of the case, and secure it from the top using M2.5x4 countersunk head screws. |
    |                                                                                                                                                               |
    | |Chapter02_93|                                                                                                                                                |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Connect the other end of the 86mm HDMI FPC Cable to the Audio-Video Board's FPC interface.                                                            |
    |                                                                                                                                                               |
    | |Chapter02_94|                                                                                                                                                |
    +---------------------------------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_92| image:: ../_static/imgs/2_Case_Assembly/Chapter02_92.png
.. |Chapter02_93| image:: ../_static/imgs/2_Case_Assembly/Chapter02_93.png
.. |Chapter02_94| image:: ../_static/imgs/2_Case_Assembly/Chapter02_94.png

2.3.5 Installing Acrylic Plates and Foot Pads
==================================================

.. table::
    :class: table-line
    :align: center
    
    +------------------------------------------------------------------------------------------------------------------------------------+
    | Step 1: Align the acrylic side plate (with the square cutout) with the GPIO headers, and secure it with M2.5x4x5 flat-head screws. |
    |                                                                                                                                    |
    | |Chapter02_95|                                                                                                                     |
    +------------------------------------------------------------------------------------------------------------------------------------+
    | Step 2: Secure the other side plate to the case with M2.5x4x5 flat-head screws                                                     |
    |                                                                                                                                    |
    | |Chapter02_96|                                                                                                                     |
    +------------------------------------------------------------------------------------------------------------------------------------+
    | Step 3: Attach the round black non-slip foot pads to the four designated mounting points on the bottom of the case.                |
    |                                                                                                                                    |
    | |Chapter02_97|                                                                                                                     |
    +------------------------------------------------------------------------------------------------------------------------------------+

.. |Chapter02_95| image:: ../_static/imgs/2_Case_Assembly/Chapter02_95.png
.. |Chapter02_96| image:: ../_static/imgs/2_Case_Assembly/Chapter02_96.png
.. |Chapter02_97| image:: ../_static/imgs/2_Case_Assembly/Chapter02_97.png
