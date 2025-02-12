import PySimpleGUI as sg
from config.styles import theme, font_settings

sg.theme(theme)

def create_main_window():
    """Creates the main window layout"""
    layout = [
        [sg.Text('Tema Principal:', font=font_settings), 
         sg.Input(key='-TOPIC-', size=(40,1))],
        [sg.Text('Indicaciones:', font=font_settings),
         sg.Multiline(key='-INSTRUCTIONS-', size=(40,5))],
        [sg.Text('Materia:', font=font_settings),
         sg.Input(key='-SUBJECT-', size=(40,1))],
        [sg.Text('Nombre:', font=font_settings),
         sg.Input(key='-NOMBRE-', size=(40,1))],
        [sg.Text('C.I.: V-', font=font_settings),
         sg.Input(key='-CI-', size=(38,1))],
        [sg.Frame('Sección', [
            [sg.Radio('Matutina (DCM)', 'SCHEDULE', key='-MORNING-', default=True),
             sg.Radio('Nocturna (DCN)', 'SCHEDULE', key='-NIGHT-')],
            [sg.Text('Trimestre:', font=font_settings),
             sg.Combo([f'{i:02}' for i in range(1, 14)], key='-TRIMESTER-', default_value='01')],
            [sg.Text('Sección Trimestre:', font=font_settings),
             sg.Combo(['01','02','03','04'], key='-SECTION-', default_value='01')]
        ], font=font_settings)],
        [sg.Frame('Evaluación', [
            [sg.Text('Número Evaluación:', font=font_settings),
             sg.Input(key='-EVAL_NUM-', size=(3,1))],
            [sg.Text('Corte:', font=font_settings),
             sg.Input(key='-CORTE-', size=(3,1))]
        ], font=font_settings)],
        [sg.Text('API:', font=font_settings),
         sg.Combo(['OpenRouter', 'Google Gemini'], key='-API-', default_value='OpenRouter', readonly=True)],
        [sg.Checkbox('Desea añadir imágenes?', key='-ADD_IMAGES-', default=True, font=font_settings)],
        [sg.Button('Generar', font=font_settings), sg.Button('Salir', font=font_settings)]
    ]
    
    window = sg.Window('Generador de Tareas Universitarias',
                    layout,
                    font=font_settings,
                    element_justification='center')
    return window
