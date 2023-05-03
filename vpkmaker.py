import os
import PySimpleGUI as sg
import json

options_file_path = os.path.join(os.getcwd(), "vpkmaker.json")
def save_options(options):
    with open(options_file_path, 'w') as f:
        json.dump(options, f)

def load_options():
    try:
        with open(options_file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

# Define the PySimpleGUI layout
options = load_options()

layout = [
    [sg.Text('Select folder to convert:')],
    [sg.InputText(key='-FOLDER-', default_text=options.get('folder', '')), sg.FolderBrowse()],
    [sg.Text('Enter vpk.exe folder:')],
    [sg.InputText(key='-VPK_PATH-', default_text=options.get('vpk_path', '')), sg.FolderBrowse()],
    [sg.Checkbox('Multi-chunk', key='-MULTI_CHUNK-', enable_events=True,default=options.get('multi_chunk', False))],
    [sg.Text('Max chunk size (MB):', key='-CHUNK_SIZE_TEXT-', visible=options.get('multi_chunk', False))],
    [sg.InputText(key='-CHUNK_SIZE-', default_text=options.get('chunk_size', '200'),visible=options.get('multi_chunk', False))],
    [sg.Button('Convert'), sg.Button('Cancel')]
]

# Create the PySimpleGUI window
window = sg.Window('VPK Maker', layout)
window.finalize()

# Event loop
while True:
    event, values = window.read()

    if event == sg.WINDOW_CLOSED or event == 'Cancel':
        break

    if event == '-MULTI_CHUNK-':
        if values['-MULTI_CHUNK-']:
            window['-CHUNK_SIZE-'].update(visible=True)
            window['-CHUNK_SIZE_TEXT-'].update(visible=True)
        else:
            window['-CHUNK_SIZE-'].update(visible=False)
            window['-CHUNK_SIZE_TEXT-'].update(visible=False)

    if event == 'Convert':
        # Get the folder path and the vpk.exe path
        options['folder'] = values['-FOLDER-']
        options['vpk_path'] = values['-VPK_PATH-']
        options['multi_chunk'] = values['-MULTI_CHUNK-']
        options['chunk_size'] = values['-CHUNK_SIZE-']
        save_options(options)

        folder_path = values['-FOLDER-']
        vpk_path = values['-VPK_PATH-']
        if values['-MULTI_CHUNK-']:
            chunk_size = values['-CHUNK_SIZE-']
        else:
            chunk_size = "1"
        if os.path.exists(folder_path) == False:
            sg.popup('Folder to convert is not exist!')
        else:
            if chunk_size.isdigit() == False:
                if chunk_size == "":
                    sg.popup('Chunk size is empty!')
                else:
                    sg.popup('Chunk size is not a number!')
            else:
                if int(chunk_size) < 0:
                    sg.popup('Chunk size is less than 0!')
                else:

                   # Build the vpk command
                    if values['-MULTI_CHUNK-']:
                        vpk_command_multichunk = " -M" + " -c " + str(chunk_size)
                    else:
                       vpk_command_multichunk = ""

                    vpk_command = "vpk" + vpk_command_multichunk + " \"" + folder_path + "\""

                    # Run the vpk command
                    os.system('chcp 65001')
                    try:
                        os.chdir(vpk_path)
                    except NotADirectoryError:
                       sg.popup('vpk.exe folder is not a folder!')
                    except FileNotFoundError:
                        sg.popup('vpk.exe folder not exist!')
                    except:
                        if vpk_path == "":
                            sg.popup('vpk.exe folder path is empty!')
                        else:
                            sg.popup('Unknown error! Check vpk.exe folder!')
                    else:
                        os.system(vpk_command)
                        sg.popup('VPK created successfully!')

# Close the PySimpleGUI window
window.close()
