import PySimpleGUI as sg
from pprint import pprint
import PyMOT.gui as gui

# Key file popup
layout = [[sg.Text('Select DVSA API key file')],
          [sg.InputText('C:/Users/Matt/Documents/mot_api.txt'), sg.FileBrowse(file_types=(("TXT Files (.txt)", "*.txt"),))],
           [sg.Submit(), sg.Cancel()]]

window = sg.Window('DVSA API key', layout)
(event, (values)) = window.Read()
keyfile = values[0]


# Event Loop
while True:
    if event is None or event == 'Exit':
        break

    if event == 'Submit':
        gui.start_main(keyfile)
        break

window.Close()

## TODO add API verification here, prompt for new key if non-functional

#def key_invalid():
#    layout = [[sg.Text('API key invalid. Please check key file and try again')],
#             [sg.Text('Select DVSA API key file')],
#             [sg.InputText(), sg.FileBrowse()],
#             [sg.Submit(), sg.Cancel()]]
#
#    (event, (keyfile,)) = sg.Window('DVSA API key', layout).Read()
#    window.Close()
