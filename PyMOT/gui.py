import PySimpleGUI as sg

from pprint import pprint
from core import api_send
from core import Vehicle
import graphics
from graphics import green_pill64
from graphics import red_pill64



sg.ChangeLookAndFeel('GreenTan')





def start_main(key):

    apikey = open(key)
    apikey = apikey.read()

# ------ Menu Definition ------ #
    menu_def = [['File', ['Open', 'Save', 'Exit', 'Properties']],
               ['Edit', ['Paste', ['Special', 'Normal', ], 'Undo'], ],
               ['Help', 'About...'], ]

# ------ Column Definition ------ #
    column1 = [[sg.Text('Column 1', background_color='#F7F3EC', justification='center', size=(10, 1))],
                [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 1')],
                [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 2')],
                [sg.Spin(values=('Spin Box 1', '2', '3'), initial_value='Spin Box 3')]]

    window = sg.Window('PyMOT 0.4.0', [
        [sg.Menu(menu_def, tearoff=True)],
        #sg.Frame(layout=[
         #   [sg.Text('MOT Validity'), title = 'MOT Information', title_color = 'red', relief = sg.RELIEF_SUNKEN]]),

    # Reg input
        [sg.Text('Vehicle registration (e.g ZZ58 ABC)')],
        [sg.InputText('', key='_REG_', size=(18, 1), focus=True, tooltip='Enter vehicle registration here'), sg.Button('Submit', bind_return_key=True), sg.Button('Exit')],
        [sg.Text('_' * 80)],

        [sg.Frame(layout=[


            #todo find out if there's a more reliable way of aligning elements for this section (might be limitation of PySimpleGUI)
            [sg.Text('Make      '), sg.InputText('None', key='_MAKE_', disabled=True, size=(22,1)),
             # 4 space
             sg.Text('    MOT Expiry'     ), sg.InputText('None', key='_EXPIRYDATE_', disabled=True, size=(18, 1))],


            [sg.Text('Model     '), sg.InputText('None', key='_MODEL_', disabled=True, size=(22,1)),
             sg.Text('    Recorded mileage'), sg.InputText('None', key='_RECMILES_', disabled=True, size=(18, 1))],

            [sg.Text('Colour     '), sg.InputText('None', key='_COLOUR_', disabled=True, size=(22,1)),
             sg.Text('    First used date'), sg.InputText('None', key='_FIRSTUSED_', disabled=True, size=(18, 1))],

            [sg.Text('Fuel Type'), sg.InputText('None', key='_FUELTYPE_', disabled=True, size=(22,1))]], title='Vehicle Information', title_color='red',
            relief=sg.RELIEF_SUNKEN, tooltip='Use these to set flags')],

        [sg.Frame(layout=[

            [sg.Text('Odometer check'), sg.Button('OK', image_data=graphics.image_file_to_bytes(green_pill64, (100,50)))]]


        , title='Vehicle Analysis', title_color='red', relief=sg.RELIEF_SUNKEN)],

        # Listbox / output
        [sg.Listbox(values=(''), size=(30, 15), key='_LIST_', enable_events=True),
         sg.Output(key='_OUTPUT_')]])



    # Event Loop
    while True:
        event, values = window.Read()
        #window.Element('_OUTPUT_').Update('Welcome to PyMOT, a Python-based MOT history analysis tool. Results from your selected MOT will appear here.')

        if event is None or event == 'Exit':
          window.Close()
          break

        if event == 'Submit':
            window.FindElement('_OUTPUT_').Update('')

            registration = values['_REG_']
            apidata = api_send(apikey, registration)
            vehicle = Vehicle(apidata)
            #pprint(vehicle.latestTest)

            testdates = mot_dates(vehicle.allTests)

            window.Element('_MAKE_').Update(vehicle.make)
            window.Element('_MODEL_').Update(vehicle.model)
            window.Element('_FUELTYPE_').Update(vehicle.fuel)
            window.Element('_COLOUR_').Update(vehicle.colour)

            # Second column in Vehicle information box
            window.Element('_EXPIRYDATE_').Update(vehicle.motExpiry)
            window.Element('_RECMILES_').Update(vehicle.latestMileage)
            window.Element('_FIRSTUSED_').Update(vehicle.firstUsedDate)

            window.Element('_LIST_').Update(testdates)

            # update analysis results
            #window.Element('_RESULTS_').Update(vehicle.latestResults)


        # Display listbox selection in table
        if event == '_LIST_' and len(values['_LIST_']):
            window.FindElement('_OUTPUT_').Update('')

            value = values['_LIST_']
            value = value[0]

            selected = iterate_tests(value, vehicle.allTests)
          #  pprint(selected)
            test_output(selected)
          #  window.Element('_RESULTS_').Update(output)




def mot_dates(tests):

    dates = []
    for test in tests:
        for k, v in test.items():
            if k == 'completedDate':
                temp = v
                dates.append(temp)

            #if k == 'testResult':
             #   temp = temp + " - " + v


    return dates


def test_output(test):
#todo add mileage from each test to output box

    commentstemp = test['rfrAndComments']

    print("Recorded mileage for this MOT: " + test['odometerValue'] + "\n")



    if len(commentstemp) == 0:
        print('Good news! No advisories or faults on this test.')

    else:

        for resultsdict in commentstemp:

            count = 0
            newfault = 1

            for key1, value1 in resultsdict.items():
                temp = []
                if key1 == 'text':
                    temp.append("Comment: " + value1)

                if key1 == 'type':
                    temp.append("Type: " + value1)

                for value in temp:
                    count = count + 1
                    # print adaption
                    #countprint = str(count)
                    print(value)

                # line space after every comment/type set
                if count & 2:
                #    newfault = newfault + 1
                 #   newfaultprint = str(newfault)

                    print("\n")
                 #   print("Fault " + newfaultprint + ")")

        #for i in value:
         #   activeVehicle.update(i)
 #       for key2, value2 in value1.items():
 #           print(type(value1))
 #           print(key2)
 #           if key2 == 'type':
  #              print("Type of fault: " + value2)
#
  #          if key2 == 'comment':
  #              print("Comment: " + value2)




def iterate_tests(target, tests):

    for test in tests:
        for k, v in test.items():
            if k == 'completedDate':
                if v == target:

                    #
                    return test

