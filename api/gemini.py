import os
import logging
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GOOGLE_GEMINI_MODEL = os.getenv("GOOGLE_GEMINI_MODEL")

LATEX_TEMPLATE = r"""
\documentclass[12pt, spanish]{article}
\usepackage[utf8]{inputenc}
\usepackage[spanish]{babel}
\usepackage{amsmath}
\usepackage{amsfonts}
\usepackage{amssymb}
\usepackage{graphicx}
\usepackage{geometry}
\geometry{a4paper, margin=2.5cm}

\title{NombreDeLaMateria}
\author{Nombre: {nombre} \\
C.I.: {ci} \\
Materia: {materia} \\
Sección: {seccion} \\
Universidad: {universidad} \\
Carrera: {carrera} \\
Evaluación: Evaluación N\textdegree{eval_num} - Corte {corte} \\
Fecha: {fecha}}
\date{}

\begin{document}

\maketitle

{contenido}

\end{document}
"""

def generate_content_gemini(topic: str, instructions: str, student_data: dict) -> str:
    """Genera contenido académico usando la API de Google Gemini"""
    try:
        genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
        model = genai.GenerativeModel(GOOGLE_GEMINI_MODEL)

        prompt = f"Genera un documento LaTeX completo en español, listo para ser compilado con pdflatex, sobre el tema: {topic}.\nInstrucciones específicas: {instructions}\n\nInstrucciones adicionales:\n- El documento debe incluir:\n  - Un encabezado con el título del tema.\n  - Estructura formal con introducción, desarrollo y conclusión.\n  - Referencias bibliográficas en formato APA.\n  - Ejemplos prácticos cuando sea aplicable.\n- No incluyas ```latex o ``` codeblocks."

        response = model.generate_content(prompt)
        generated_text = response.text.replace('&', '\\&')
        logging.info(f"Contenido generado exitosamente con Gemini. Longitud: {len(generated_text)} caracteres")

        latex_content = LATEX_TEMPLATE.format(
            nombre=student_data['nombre'],
            ci=student_data['ci'],
            materia=student_data['materia'],
            seccion=student_data['seccion'],
            universidad=student_data['universidad'],
            carrera=student_data['carrera'],
            eval_num=student_data['eval_num'],
            corte=student_data['corte'],
            fecha=student_data['fecha'],
            contenido=generated_text
        )

        return latex_content

    except Exception as e:
        logging.error(f"Error en la API de Gemini: {str(e)}")
        raise Exception(f"Error al comunicarse con Google Gemini: {str(e)}")
