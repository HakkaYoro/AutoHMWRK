import logging
import os
from datetime import datetime
import FreeSimpleGUI as sg
from api.openai_client import generate_content_openai
from api.gemini import generate_content_gemini
from utils.validators import validate_ci, validate_section
from utils.image_scraper import download_images
import subprocess
from config.styles import font_settings
from utils import build_student_data

def handle_generate_event(window, values):
    """Handles the task generation event"""
    try:
        # Validate inputs
        if not validate_inputs(values):
            return

        # Generar contenido con API
        logging.info("Generando contenido con API...")
        student_data = build_student_data(values)
        
        provider = values.get('-API-PROVIDER-', 'OpenRouter')
        full_content = ""
        
        if provider == 'Google Gemini':
            # Use Native Gemini implementation (legacy but functional)
            logging.info("Using Google Gemini Native Provider")
            full_content = generate_content_gemini(
                values['-TOPIC-'],
                values['-INSTRUCTIONS-'],
                student_data
            )
        
        elif provider == 'OpenRouter':
            # Use OpenAI Client but with OpenRouter env vars
            logging.info("Using OpenRouter Provider via OpenAI Client")
            
            api_key = os.getenv("OPENROUTER_API_KEY")
            model = os.getenv("OPENROUTER_MODEL")
            # OpenRouter standard URL
            base_url = "https://openrouter.ai/api/v1" 
            
            # Allow override via env if needed, but hardcoding standard is safer for 'OpenRouter' preset
            if not api_key:
                raise ValueError("Falta OPENROUTER_API_KEY en el archivo .env")
                
            full_content = generate_content_openai(
                topic=values['-TOPIC-'],
                instructions=values['-INSTRUCTIONS-'],
                student_data=student_data,
                api_key=api_key,
                base_url=base_url,
                model=model,
                enable_reasoning_filter=False # Usually not needed unless specific model
            )
            
        elif provider == 'OpenAI / Custom':
            # Use generic variables
            logging.info("Using OpenAI / Custom Provider")
            
            api_key = os.getenv("OPENAI_API_KEY")
            base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
            model = os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")
            
            # Parse boolean from env
            filter_reasoning_env = os.getenv("REASONING_FILTER", "false")
            filter_reasoning = filter_reasoning_env.lower() in ('true', '1', 't', 'yes')

            if not api_key:
                raise ValueError("Falta OPENAI_API_KEY en el archivo .env")

            full_content = generate_content_openai(
                topic=values['-TOPIC-'],
                instructions=values['-INSTRUCTIONS-'],
                student_data=student_data,
                api_key=api_key,
                base_url=base_url,
                model=model,
                enable_reasoning_filter=filter_reasoning
            )

        # Descargar imágenes
        image_paths = []
        if values['-ADD_IMAGES-']:
            logging.info("Buscando imágenes relacionadas...")
            try:
                # Usar el tema principal para buscar imágenes, es más preciso que el contenido completo
                search_query = values['-TOPIC-']
                # Si hay materia, combinarla para contexto
                if values['-SUBJECT-']:
                    search_query += f" {values['-SUBJECT-']}"
                
                image_paths = download_images(search_query, "temp_images")
            except Exception as img_err:
                 logging.warning(f"No se pudieron descargar imágenes: {img_err}")


        # Guardar el contenido LaTeX en un archivo temporal
        output_dir = "generated_docs"
        os.makedirs(output_dir, exist_ok=True)
        filename = f"{build_section_code(values)}_{datetime.now().strftime('%Y%m%d%H%M%S')}.tex"
        filepath = os.path.join(output_dir, filename)

        # Remove code blocks if still present
        if full_content:
            full_content = full_content.replace("```latex", "").replace("```", "")
            
            # Inject images if any
            if image_paths:
                full_content = inject_images(full_content, image_paths)
        else:
            raise ValueError("La API no devolvió contenido.")

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
            
            if process.returncode != 0:
                logging.error(f"Salida de LaTeX (stderr): {stderr.decode('utf-8')}")
                raise Exception(f"Error LaTeX: {stderr.decode('utf-8')[-300:]}")

            # Renombrar el PDF
            pdf_path = os.path.splitext(filepath)[0] + ".pdf"
            student_data = build_student_data(values)
            new_pdf_name = (
                f"{student_data['nombre']} - V{student_data['ci']} - "
                f"{student_data['materia']} - {student_data['seccion']} - "
                f"Ev. {student_data['eval_num']} Corte {student_data['corte']} - UAH.pdf"
            )
            # Sanitize filename
            new_pdf_name = "".join([c for c in new_pdf_name if c.isalnum() or c in (' ', '-', '.', '_')]).strip()
            new_pdf_path = os.path.join(os.path.dirname(filepath), new_pdf_name)
            
            os.rename(pdf_path, new_pdf_path)
            logging.info("PDF compilado y renombrado exitosamente.")
            sg.popup_ok(f"Tarea generada exitosamente!\nPDF: {new_pdf_path}", font=font_settings)
            
        except Exception as e:
            logging.error(f"Error al compilar LaTeX: {str(e)}")
            sg.popup_error(f"Error compilación: {str(e)}", font=font_settings)

    except Exception as e:
        logging.error(f"Error al generar tarea: {str(e)}")
        sg.popup_error(f"Error general: {str(e)}", font=font_settings)

def inject_images(content: str, image_paths: list) -> str:
    """Injects images into the LaTeX content before the end of the document"""
    if not image_paths:
        return content
        
    image_section = "\n\n\\section*{Anexos Gráficos}\n"
    
    for i, path in enumerate(image_paths):
         # path is usually like "temp_images/img_testtest_0.jpg"
         # Since we compile inside generated_docs/, we need "../" to go back to root
         # Ensure we use forward slashes for LaTeX
         relative_path = "../" + path.replace(os.sep, '/')
         
         # Use float barrier or clearpage to prevent messy layout
         image_section += "\\begin{figure}[h!]\n\\centering\n"
         image_section += f"\\includegraphics[width=0.75\\textwidth]{{{relative_path}}}\n"
         image_section += f"\\caption{{Imagen ilustrativa {i+1}}}\n"
         image_section += "\\end{figure}\n\\clearpage\n"
    
    if "\\end{document}" in content:
        return content.replace("\\end{document}", image_section + "\\end{document}")
    else:
        return content + image_section

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
        'tema': values['-TOPIC-'] 
    }
    return student_data

def build_section_code(values):
    """Construye el código de sección DCM/DCN + trimestre + sección"""
    turno = "DCM" if values['-MORNING-'] else "DCN"
    return f"{turno}{values['-TRIMESTER-']}{values['-SECTION-']}"

def handle_exit_event(window):
    """Handles the exit event"""
    window.close()
