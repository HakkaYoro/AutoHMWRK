import os
import logging
import re
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()

def generate_content_openai(
    topic: str, 
    instructions: str, 
    student_data: dict, 
    api_key: str = None, 
    base_url: str = None, 
    model: str = None,
    enable_reasoning_filter: bool = False
) -> str:
    """Generates LaTeX content using an OpenAI-compatible API."""
    try:
        # Configuration
        # If arguments are provided (from GUI), use them. Otherwise, fall back to ENV.
        final_api_key = api_key or os.getenv("OPENAI_API_KEY")
        final_base_url = base_url or os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1")
        final_model = model or os.getenv("OPENAI_MODEL", "gpt-3.5-turbo")

        if not final_api_key:
            raise ValueError("API Key is required. Please set it in the settings or .env file.")

        logging.info(f"Connecting to OpenAI API at {final_base_url} with model {final_model}")

        client = OpenAI(
            api_key=final_api_key,
            base_url=final_base_url,
        )

        prompt = (
            "Actúa como un experto académico y diseñador de LaTeX. Tu tarea es generar el código fuente LaTeX para un trabajo universitario."
            "REQUISITOS CRÍTICOS:\n"
            "1. NO devuelvas bloques de código markdown (no uses ```latex). Devuelve SÓLO el código puro.\n"
            "2. El documento debe compilar correctamente con 'pdflatex'.\n"
            "3. Usa paquetes estándar y compatibles. Para el idioma español, usa \\usepackage[spanish]{babel} (sin opciones extra como es-tabla si causan error).\n"
            "4. NO incluyas \\maketitle ni índices (\\tableofcontents).\n"
            "5. NO numeres las secciones (usa \\section*{}).\n"
            "6. El contenido debe ser EXTENSO, con introducciones, desarrollo detallado, ejemplos y conclusiones.\n"
            "\n"
            "--- DATOS DEL ESTUDIANTE ---\n"
            f"Nombre: {student_data['nombre']}\n"
            f"C.I.: {student_data['ci']}\n"
            f"Materia: {student_data['materia']}\n"
            f"Sección: {student_data['seccion']}\n"
            f"Universidad: {student_data['universidad']}\n"
            f"Carrera: {student_data['carrera']}\n"
            f"Evaluación: Evaluación N° {student_data['eval_num']} - Corte {student_data['corte']}\n"
            f"Fecha: {student_data['fecha']}\n"
            "\n"
            "--- TEMA Y CONTENIDO ---\n"
            f"Tema Principal: {topic}\n"
            f"Instrucciones: {instructions}\n"
            "\n"
            "--- ESTRUCTURA ---\n"
            "1. Portada Personalizada: Usa el marcador %%PROJECT_LOGO_PATH%% para el logo (tamaño 4cm).\n"
            "2. Introducción: Al menos 2 párrafos.\n"
            "3. Desarrollo: Varias secciones (sin numerar). Usa negritas, listas y cursivas para dar formato profesional.\n"
            "4. Si es relevante, incluye alguna tabla simple.\n"
            "5. Conclusión.\n"
        )

        response = client.chat.completions.create(
            model=final_model,
            messages=[
                {"role": "system", "content": "You are a helpful academic assistant capable of generating high-quality compiled LaTeX code."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )

        generated_text = response.choices[0].message.content

        # Handle Reasoning Tags (e.g., DeepSeek <think>)
        if enable_reasoning_filter:
            logging.info("Applying reasoning filter (<think> tags)...")
            # Remove content between <think> and </think> including the tags
            generated_text = re.sub(r'<think>.*?</think>', '', generated_text, flags=re.DOTALL)
            # Also remove just the tags if they appear without closing/opening pair issues, just in case
            generated_text = generated_text.replace("<think>", "").replace("</think>", "")

        # Post-processing: Replace Logo Placeholder
        generated_text = generated_text.replace("%%PROJECT_LOGO_PATH%%", "../logos/UAH.png")
        
        logging.info(f"Content generated successfully. Length: {len(generated_text)} chars")
        return generated_text

    except Exception as e:
        logging.error(f"OpenAI API Error: {str(e)}")
        raise Exception(f"Failed to communicate with API: {str(e)}")
