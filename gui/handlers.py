import logging
import os
from datetime import datetime
import PySimpleGUI as sg
from api.openrouter import generate_content
from api.gemini import generate_content_gemini
from utils.validators import validate_ci, validate_section
from utils.image_scraper import download_images
import subprocess
from config.styles import font_settings
from utils import build_student_data  # Ahora se importa correctamente desde utils/__init__.py

def handle_generate_event(window, values):
    """Handles the task generation event"""
    try:
        # Validate inputs
        if not validate_inputs(values):
            return

        # Generar contenido con API
        logging.info("Generando contenido con API...")
        student_data = build_student_data(values)
        if values['-API-'] == 'OpenRouter':
            full_content = generate_content(
                values['-TOPIC-'],
                values['-INSTRUCTIONS-'],
                student_data
            )
        elif values['-API-'] == 'Google Gemini':
            full_content = generate_content_gemini(
                values['-TOPIC-'],
                values['-INSTRUCTIONS-'],
                student_data
            )
        else:
            raise ValueError("API no válida")

        # Descargar imágenes
        image_paths = []
        if values['-ADD_IMAGES-']:
            logging.info("Buscando imágenes relacionadas...")
            image_paths = download_images(full_content, "temp_images")

        # Guardar el contenido LaTeX en un archivo temporal
        output_dir = "generated_docs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{build_section_code(values)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.tex"
        filepath = os.path.join(output_dir, filename)

        # Remove code blocks
        full_content = full_content.replace("```latex", "")
        full_content = full_content.replace("```", "")

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(full_content)

        # Compilar a PDF
        logging.info("Compilando a PDF...")
        try:
            command = ["pdflatex", "-halt-on-error", os.path.basename(filepath)]
            cwd = os.path.dirname(filepath)
            logging.info(f"Ejecutando comando LaTeX: {' '.join(command)}")
            process = subprocess.Popen(command, cwd=cwd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            stdout, stderr = process.communicate()

            logging.info(f"Salida de LaTeX (stdout): {stdout.decode('utf-8')}")
            logging.error(f"Salida de LaTeX (stderr): {stderr.decode('utf-8')}")

            if process.returncode != 0:
                logging.error(f"Error al compilar LaTeX: {stderr.decode('utf-8')}")
                raise Exception(f"Error al compilar LaTeX: {stderr.decode('utf-8')}")

            # Renombrar el PDF según la estructura solicitada:
            # (Nombre del Estudiante) - V(Número de cédula) - (Materia) - (Sección) - Ev. (Número de Evaluación) Corte (Número de corte) - UAH.pdf
            pdf_path = os.path.splitext(filepath)[0] + ".pdf"
            student_data = build_student_data(values)
            new_pdf_name = (
                f"{student_data['nombre']} - V{student_data['ci']} - "
                f"{student_data['materia']} - {student_data['seccion']} - "
                f"Ev. {student_data['eval_num']} Corte {student_data['corte']} - UAH.pdf"
            )
            new_pdf_path = os.path.join(os.path.dirname(filepath), new_pdf_name)
            os.rename(pdf_path, new_pdf_path)
            logging.info("PDF compilado y renombrado exitosamente.")
            sg.popup_ok(f"Tarea generada exitosamente!\nPDF: {new_pdf_path}",
                       font=font_settings)
        except Exception as e:
            logging.error(f"Error al compilar LaTeX: {str(e)}")
            logging.debug(f"Error al compilar LaTeX: {str(e)}", exc_info=True)
            sg.popup_error(f"Error: {str(e)}", font=font_settings)

    except Exception as e:
        logging.error(f"Error al generar tarea: {str(e)}")
        logging.debug(f"Error al generar tarea: {str(e)}", exc_info=True)
        sg.popup_error(f"Error: {str(e)}", font=font_settings)

def validate_inputs(values):
    """Valida todos los campos de entrada"""
    errors = []
    
    if not values['-TOPIC-']:
        errors.append("Debe ingresar un tema principal")
    
    if not values['-INSTRUCTIONS-']:
        errors.append("Debe ingresar indicaciones")
    
    
    section_code = build_section_code(values)
    if not validate_section(section_code):
        errors.append("Código de sección inválido")
    
    if errors:
        sg.popup_error("\n".join(errors), font=font_settings)
        return False
    
    return True

def build_student_data(values):
    """Construye los datos del estudiante para el encabezado"""
    student_data = {
        'nombre': values['-NOMBRE-'],
        'ci': "V-" + values['-CI-'],
        'materia': values['-SUBJECT-'],
        'seccion': build_section_code(values),
        'universidad': "Universidad Alejandro de Humboldt",
        'carrera': "Ing. En Informática",
        'eval_num': values['-EVAL_NUM-'],
        'corte': values['-CORTE-'],
        'fecha': datetime.now().strftime("%d/%m/%Y"),
        'tema': values['-TOPIC-'] # Add topic to student data
    }
    return student_data

def build_section_code(values):
    """Construye el código de sección DCM/DCN + trimestre + sección"""
    turno = "DCM" if values['-MORNING-'] else "DCN"
    return f"{turno}{values['-TRIMESTER-']}{values['-SECTION-']}"

def handle_exit_event(window):
    """Handles the exit event"""
    window.close()
