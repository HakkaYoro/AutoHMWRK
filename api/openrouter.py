import os
import logging
import requests
from dotenv import load_dotenv

load_dotenv()

API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {os.getenv('OPENROUTER_API_KEY')}",
    "HTTP-Referer": "https://github.com/user/proyecto_tareas",
    "X-Title": "Generador de Tareas Universitarias"
}

def generate_content(topic: str, instructions: str, student_data: dict) -> str:
    """Genera contenido académico usando la API de OpenRouter"""
    try:
        prompt = f"Genera un documento LaTeX completo en español, listo para ser compilado con pdflatex, sobre el tema: {topic}.\nInstrucciones específicas: {instructions}\n\nInstrucciones adicionales:\n- El documento debe incluir:\n  - Un encabezado con el título del tema.\n  - Estructura formal con introducción, desarrollo y conclusión.\n  - Referencias bibliográficas en formato APA.\n  - Ejemplos prácticos cuando sea aplicable.\n- No incluyas ```latex o ``` codeblocks.\n- Usa '\\&' en lugar de '&' en las referencias bibliográficas."
        
        payload = {
            "model": os.getenv("OPENROUTER_MODEL"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        generated_text = response.json()["choices"][0]["message"]["content"]
        logging.info(f"Contenido generado exitosamente. Longitud: {len(generated_text)} caracteres")

        latex_content = LATEX_TEMPLATE.format(
            nombre=student_data['nombre'],
            ci=student_data['ci'],
            materia=student_data['materia'],
            seccion=student_data['seccion'],
            universidad=student_data['universidad'],
            carrera=student_data['carrera'],
            eval_num=student_data['eval_num'],
            corte=student_data['corte'],
            fecha=student_data['fecha']
        )

        return latex_content

    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la API: {str(e)}")
        raise Exception(f"Error al comunicarse con OpenRouter: {str(e)}")
    except KeyError as e:
        logging.error("Respuesta inesperada de la API")
        raise Exception("La API devolvió una respuesta no válida")

LATEX_TEMPLATE = r"""
\documentclass[12pt, spanish]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}

\begin{document}

\noindent
Nombre: {nombre} \\
C.I.: {ci} \\
Materia: {materia} \\
Sección: {seccion} \\
Universidad: {universidad} \\
Carrera: {carrera} \\
Evaluación: Evaluación N\textdegree{eval_num} - Corte {corte} \\
Fecha: {fecha}

\vspace{2cm}
\begin{center}
\end{center}

{contenido}

\end{document}
"""

def generate_content(topic: str, instructions: str) -> str:
    """Genera contenido académico usando la API de OpenRouter"""
    try:
        prompt = f"Genera el contenido LaTeX en español, listo para ser compilado con pdflatex, sobre el tema: {topic}.\nInstrucciones específicas: {instructions}\n\nInstrucciones adicionales:\n- El contenido del documento debe incluir:\n  - Estructura formal con introducción, desarrollo y conclusión.\n  - Referencias bibliográficas en formato APA.\n  - Ejemplos prácticos cuando sea aplicable.\n- No incluyas ninguna información adicional como encabezados, pie de página o cualquier otra información que no sea el contenido principal del documento.\n- No incluyas ```latex o ``` codeblocks.\n- Usa '\\&' en lugar de '&' en las referencias bibliográficas."
        
        payload = {
            "model": os.getenv("OPENROUTER_MODEL"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()
        
        generated_text = response.json()["choices"][0]["message"]["content"]
        logging.info(f"Contenido generado exitosamente. Longitud: {len(generated_text)} caracteres")
        return generated_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la API: {str(e)}")
        raise Exception(f"Error al comunicarse con OpenRouter: {str(e)}")
    except KeyError as e:
        logging.error("Respuesta inesperada de la API")
        raise Exception("La API devolvió una respuesta no válida")
