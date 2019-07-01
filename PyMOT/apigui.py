import PyMOT.core as core
import PySimpleGUI as sg
from pprint import pprint
import PyMOT.gui as gui

# Key file popup
layout = [[sg.Text('Select DVSA API key file')],
          # todo remove default text below before upload
           [sg.InputText('C:/Users/Matt/Documents/GitHub/PyMOT/data/mot_api.txt'), sg.FileBrowse(file_types=(("TXT Files (.txt)", "*.txt"),))],
           [sg.Submit(), sg.Cancel()]]

#
(event, (values)) = sg.Window('DVSA API key', layout).Read()
keyfile = values[0]


# Event Loop
while True:
  if event is None or event == 'Exit':
      # TODO fix program close, currently reopens itself
      #window.Close()
      break

  if event == 'Submit':
        gui.start_main(keyfile)



## TODO add API verification here, prompt for new key if non-functional

#def key_invalid():
#    layout = [[sg.Text('API key invalid. Please check key file and try again')],
#             [sg.Text('Select DVSA API key file')],
#             [sg.InputText(), sg.FileBrowse()],
#             [sg.Submit(), sg.Cancel()]]
#
#    (event, (keyfile,)) = sg.Window('DVSA API key', layout).Read()
#    window.Close()


# Main window

#layout = [[sg.Text('Vehicle registration:'), sg.Text('', key='_REG_')],
#          [sg.Input(do_not_clear=True, key='_IN_')],
#          [sg.Button('Submit'), sg.Button('Exit')]]
#
#window = sg.Window('PyMOT', layout)





#core.api_send()