import logging
import os
from dotenv import load_dotenv
import PySimpleGUI as sg
from api.openrouter import generate_content
from utils.logger import setup_logger
from utils.validators import validate_ci, validate_section
from gui.layout import create_main_window
from gui.handlers import handle_generate_event, handle_exit_event

load_dotenv()
setup_logger()

def main():
    window = create_main_window()
    
    while True:
        event, values = window.read()
        
        if event == sg.WIN_CLOSED or event == 'Salir':
            handle_exit_event(window)
            break
            
        if event == 'Generar':
            handle_generate_event(window, values)
            
    window.close()

if __name__ == "__main__":
    main()
