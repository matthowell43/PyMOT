# Powered by PySimpleGUI module which is licensed under LGPL v3.
# Icon made by itim2101 on www.flaticon.com (https://www.flaticon.com/free-icon/maintenance_1967734)

import PySimpleGUI as sg

#print = sg.EasyPrint

from pprint import pprint
import PyMOT.core as core
from PyMOT.core import api_send
from PyMOT.core import Vehicle

import PyMOT.graphics as graphics
from PyMOT.graphics import green_pill64
from PyMOT.graphics import red_pill64
import PyMOT.analysis as analysis

# Window theme
sg.ChangeLookAndFeel('GreenTan')

def start_main(key):

    apikey = open(key)
    apikey = apikey.read()

# ------ Menu Definition ------ #
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
               ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
               ['Help', 'About...'], ]

# ------ Window Definition ------ #
    # todo find out if there's a more reliable way of aligning elements for this section (might be limitation of PySimpleGUI)

    window = sg.Window('PyMOT 0.4.1', [
        [sg.Menu(menu_def, tearoff=True)],

        # Reg input
        [sg.Text('Vehicle registration (e.g ZZ58 ABC)')],
        [sg.InputText('', key='_REG_', size=(18, 1), focus=True, tooltip='Enter vehicle registration here'), sg.Button('Submit', bind_return_key=True), sg.Button('Exit', key='_EXIT_')],
        [sg.Text('_' * 80)],
        # Vehicle info
        [sg.Frame(layout=[
            [sg.Text('Make      '), sg.InputText('None', key='_MAKE_', disabled=True, size=(22,1)),
             # 4 space
             sg.Text('    MOT Expiry'     ), sg.InputText('None', key='_EXPIRYDATE_', disabled=True, size=(18, 1))],

            [sg.Text('Model     '), sg.InputText('None', key='_MODEL_', disabled=True, size=(22,1)),
             sg.Text('    Recorded mileage'), sg.InputText('None', key='_RECMILES_', disabled=True, size=(18, 1))],

            [sg.Text('Colour     '), sg.InputText('None', key='_COLOUR_', disabled=True, size=(22,1)),
             sg.Text('    First used date'), sg.InputText('None', key='_FIRSTUSED_', disabled=True, size=(18, 1))],

            [sg.Text('Fuel Type'), sg.InputText('None', key='_FUELTYPE_', disabled=True, size=(22,1))]], title='Vehicle Information', title_color='red',
            relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],
        # Vehicle analysis elements
        [sg.Frame(layout=[

            [sg.Text('Odometer check'), sg.Button('OK', image_data=graphics.image_file_to_bytes(green_pill64, (80, 40)), key='_ODOMETER_', font='Any 12', pad=(0,0)),
             sg.Text('     Recurring faults'), sg.Button('OK', image_data=graphics.image_file_to_bytes(green_pill64, (80, 40)), key='_RECURRING_', font='Any 12', pad=(0,0))],

            # Safety issues button
            [sg.Text('Safety issues    '), sg.Button('OK', image_data=graphics.image_file_to_bytes(green_pill64, (80, 40)), key='_SAFETY_', font='Any 12', pad=(0, 0)),]]

            , title='Vehicle Analysis', title_color='red', relief=sg.RELIEF_SUNKEN)],

        # Listbox / output
        [sg.Listbox(values=(''), size=(30, 15), key='_LIST_', enable_events=True),
         sg.Output(key='_OUTPUT_')]])


    # Event Loop
    while True:
        event, values = window.Read()

        if event in (None, '_EXIT_'):
          break

        if event == 'Submit':
            window.FindElement('_OUTPUT_').Update('')
            registration = values['_REG_']
            apidata = api_send(apikey, registration)
            vehicle = Vehicle(apidata)

            if vehicle.invalidReg == False:
                window.Element('_MAKE_').Update(vehicle.make)
                window.Element('_MODEL_').Update(vehicle.model)
                window.Element('_FUELTYPE_').Update(vehicle.fuel)
                window.Element('_COLOUR_').Update(vehicle.colour)

            if vehicle.allTests is not None:
                window.Element('_FIRSTUSED_').Update(vehicle.firstUsedDate)
                testdates = mot_dates(vehicle.allTests)
                window.Element('_RECMILES_').Update(vehicle.latestMileage)

                window.Element('_LIST_').Update(testdates)

                # FaultScanner test
                # todo fix

                #if vehicle.faultScanner.faultDictList is None:
                #    print("No faults detected by FaultScanner !")

                if vehicle.faultScanner.brakeFaultsDetected is not None:
                    print("Brake fault(s) detected. \n Terms found in test comments: ")
                    #for fault in vehicle.faultScanner.brakeFaultsDetected:
                    #    print(fault)

                    # debug
                    #print(vehicle.faultScanner.brakeFaultsDetected)


            if vehicle.motExpiry is not None:
                window.Element('_EXPIRYDATE_').Update(vehicle.motExpiry)

            if vehicle.recurringFaultsPresent == True:
                window.Element('_RECURRING_').Update('Alert',
                                                    image_data=graphics.image_file_to_bytes(red_pill64, (80, 40)),)

            else:
                window.Element('_RECURRING_').Update('OK',
                                                     image_data=graphics.image_file_to_bytes(green_pill64, (80, 40)))

            if vehicle.clockedCheck == False:
                window.Element('_ODOMETER_').Update('Alert',
                                                      image_data=graphics.image_file_to_bytes(red_pill64, (80, 40)))

            # FaultScanner implementation via popup

            ## TODO add button in gui
            #sg.Popup('Vehicle Report PLACEHOLDER - WIP', '',
            #         'Total Brake faults detected: ' + str(scanner.brakeFaultsTotal),
             #        '----- Brake faults in latest MOT: ' + str(scanner.brakeFaultsLatest),
             #        '',
             #        'Total Suspension faults detected: ' + str(scanner.suspensionFaultsTotal),
             #        '----- Suspension faults in latest MOT: ' + str(scanner.suspensionFaultsLatest))

        # Details upon clicking Odometer check button
        if event == '_ODOMETER_':

            if vehicle.clockedCheck == False:
                window.Element('_ODOMETER_').Update('Alert',
                                                      image_data=graphics.image_file_to_bytes(red_pill64, (80, 40)))

                window.FindElement('_OUTPUT_').Update('')

                print('Odometer report: ALERT - Issues detected \n' )
                print('WARNING: Inconsistent odometer values have been detected.')
                print("This *might* indicate that the vehicle's odometer has been modified. \n")

                odometerlist = []
                datelist = []
                for test in vehicle.allTests:

                    for k, v in test.items():
                        if k == 'completedDate':
                            datelist.append(v)
                        if k == 'odometerValue':
                            odometerlist.append(v)

                for (date, odometer) in zip(datelist, odometerlist):
                    print('Date: ' + date + " - Mileage: " + odometer + "\n")

            else:
                window.FindElement('_OUTPUT_').Update('')
                odometerlist = []
                datelist = []
                print("Odometer report: No issues detected\n")
                for test in vehicle.allTests:

                    for k, v in test.items():
                        if k == 'completedDate':
                            datelist.append(v)
                        if k == 'odometerValue':
                            odometerlist.append(v)

                for (date, odometer) in zip(datelist, odometerlist):
                    print('Date: ' + date + " - Mileage: " + odometer + "\n")

        # Display listbox selection in output box
        if event == '_LIST_' and len(values['_LIST_']):
            window.FindElement('_OUTPUT_').Update('')
            value = values['_LIST_']
            value = value[0]

            selected = iterate_tests(value, vehicle.allTests)

            test_output(selected)

        # Safety issues element
        if event == '_SAFETY_':
            window.FindElement('_OUTPUT_').Update('')

            safety_issues_output(vehicle.faultScanner.safetyFaultsDetected, vehicle.faultScanner.brakeFaultsDetected)



    window.Close()

def mot_dates(tests):

    dates = []
    for test in tests:
        for k, v in test.items():
            if k == 'completedDate':
                temp = v
                dates.append(temp)

    return dates


def test_output(test):

    commentstemp = test['rfrAndComments']

    print("Recorded mileage for this MOT: " + test['odometerValue'] + "\n")

    if len(commentstemp) == 0:
        print('Good news! No advisories or faults on this test.')

    else:
        for resultsdict in commentstemp:

            count = 0

            for key1, value1 in resultsdict.items():
                temp = []
                if key1 == 'text':
                    temp.append("Comment: " + value1)

                if key1 == 'type':
                    temp.append("Type: " + value1)

                for value in temp:
                    count = count + 1
                    # print adaption
                    print(value)

                # line space after every comment/type set
                if count & 2:
                    print("\n")


def iterate_tests(target, tests):

    for test in tests:
        for k, v in test.items():
            if k == 'completedDate' and v == target:
                return test

def safety_issues_output(safety, brakes):
    # latest MOT only
    safety_latest = safety[0]
    brakes_latest = brakes[0]
    print("Safety issues have been detected in the latest MOT for this vehicle. \n")
    print("Advice: Repair these items immediately.\n --- If the braking system is mentioned below, have the vehicle serviced by a qualified mechanic as soon as possible.")
    print("Safety issues in latest MOT: \n")
    for k, v in safety_latest.items():
        #access comment set
        for comment in v:
            if len(comment) > 0:
                print("- - " + comment + "\n")

    print("Braking system issues detected: \n ")
    for k, v in brakes_latest.items():
        #access comment set
        for comment in v:
            if len(comment) > 0:
                print("- - " + comment + "\n")








# todo place all gui tests in this method
def output_test():
    return None
