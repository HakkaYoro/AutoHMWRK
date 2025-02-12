import os
import logging
import re
import google.generativeai as genai
from dotenv import load_dotenv

load_dotenv()

GOOGLE_GEMINI_API_KEY = os.getenv("GOOGLE_GEMINI_API_KEY")
GOOGLE_GEMINI_MODEL = os.getenv("GOOGLE_GEMINI_MODEL")

# Eliminar este bloque si ya no se utiliza
#LATEX_TEMPLATE = r"""
#\documentclass{{article}}
#...
#\end{{document}}
#"""{{document}}


def generate_content_gemini(topic: str, instructions: str, student_data: dict) -> str:
    """Genera un documento LaTeX completo, detallado y listo para compilar, usando la API de Google Gemini.
    Se usa el marcador %%PROJECT_LOGO_PATH%% para la ruta del logo, que luego se reemplaza por la ruta relativa correcta."""
    try:
        genai.configure(api_key=GOOGLE_GEMINI_API_KEY)
        model = genai.GenerativeModel(GOOGLE_GEMINI_MODEL)

        prompt = (
            "Diseña un documento LaTeX completo, elegante, profesional y muy detallado. "
            "El contenido debe ser extenso y completo, con explicaciones profundas y ejemplos cuando corresponda. "
            "El documento debe compilarse sin errores con pdflatex y no debe incluir tabla de contenidos ni texto de ejemplo como Lorem Ipsum. "
            "Devuelve únicamente el código LaTeX. "
            "Utiliza un preámbulo moderno, una portada llamativa y secciones claras. "
            "Recuerda que los títulos de las secciones no deben llevar numeración. Por ejemplo, en lugar de '2 Estándar ISO/IEC 25010' "
            "y '2.1 Características de la Calidad del Producto', simplemente usa 'Estándar ISO/IEC 25010' y 'Características de la Calidad del Producto'.\n\n"
            "--- Información del Documento ---\n"
            f"Tema: {topic}\n"
            f"Instrucciones: {instructions}\n\n"
            "--- Información del Estudiante ---\n"
            f"Nombre: {student_data['nombre']}\n"
            f"C.I.: {student_data['ci']}\n"
            f"Materia: {student_data['materia']}\n"
            f"Sección: {student_data['seccion']}\n"
            f"Universidad: {student_data['universidad']}\n"
            f"Carrera: {student_data['carrera']}\n"
            f"Evaluación: Evaluación N° {student_data['eval_num']} - Corte {student_data['corte']}\n"
            f"Fecha: {student_data['fecha']}\n\n"
            "Requisitos adicionales:\n"
            " - La portada debe incluir el logo de la Universidad. Usa el marcador %%PROJECT_LOGO_PATH%% en el comando "
            "de \\includegraphics, para que luego se reemplace automáticamente por la ruta relativa correcta "
            "(teniendo en cuenta que el archivo se compila desde la carpeta generated_docs).\n"
            " - No incluir tabla de contenidos ni secciones con Lorem Ipsum.\n"
            " - No agregar comentarios o texto extra fuera del código LaTeX.\n"
            " - Asegúrate de que el contenido generado sea largo, completo y detallado, sin numerar los títulos de las secciones."
        )

        response = model.generate_content(prompt)
        latex_content = response.text

        # La compilación se realiza desde la carpeta "generated_docs", por lo que la ruta relativa al logo debe ser "../logos/UAH.png"
        latex_content = latex_content.replace("%%PROJECT_LOGO_PATH%%", "../logos/UAH.png")
        logging.info(f"Contenido generado exitosamente con Gemini. Longitud: {len(latex_content)} caracteres")
        return latex_content

    except Exception as e:
        logging.error(f"Error en la API de Gemini: {str(e)}")
        raise Exception(f"Error al comunicarse con Google Gemini: {str(e)}")
