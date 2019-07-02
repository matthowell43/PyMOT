# PyMOT - a Python-based vehicle MOT checker

PyMOT is intended for UK car owners or prospective buyers who wish to examine a vehicle's MOT history in detail. It uses a DVSA (DVLA digital service) API key to pull vehicle data from the DVSA servers which is then processed by this application. The GUI is implemented via use of PySimpleGUI (Tkinter version).

The license for this API key currently prevents me from including it in this program, but keys are freely available via this link: https://www.smartsurvey.co.uk/s/MOT_History_TradeAPI_Access_and_Support? - PyMOT will ask for an API key from a .TXT file on startup- it will not function without one.

My goal with this application is for it to be a superior version of the Gov.uk web tool for MOT history. It will display all MOT's in a simple way, thereby allowing users to examine a vehicle easily. 

PyMOT will notify the user of any potentially serious defects such as evidence of odometer modification ('clocking' a car) or recurring faults which may indicate neglect by previous owner(s). In short, it will utilise every aspect of the available data to ensure users are as well informed as possible.
