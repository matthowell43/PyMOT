import PyMOT.gui as gui
import PySimpleGUI as sg
# Icon made by itim2101 on www.flaticon.com (https://www.flaticon.com/free-icon/maintenance_1967734)

def start_api_gui():

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
            gui.Interface(keyfile)
            break

    window.Close()


start_api_gui()

## TODO add API verification here, prompt for new key if non-functional

#def key_invalid():
#    layout = [[sg.Text('API key invalid. Please check key file and try again')],
#             [sg.Text('Select DVSA API key file')],
#             [sg.InputText(), sg.FileBrowse()],
#             [sg.Submit(), sg.Cancel()]]
#
#    (event, (keyfile,)) = sg.Window('DVSA API key', layout).Read()
#    window.Close()
