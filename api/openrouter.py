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

# Eliminar este bloque si ya no se utiliza
#LATEX_TEMPLATE = r"""
#\documentclass{{article}}
#...
#\end{{document}}
#"""

def generate_content(topic: str, instructions: str, student_data: dict) -> str:
    """Genera un documento LaTeX completo, detallado y listo para compilar.
    Se utiliza el marcador %%PROJECT_LOGO_PATH%% para indicar la ubicación del logo, que luego se reemplaza por la ruta relativa correcta."""
    try:
        prompt = (
            "Diseña un documento LaTeX completo, elegante, profesional y muy detallado. "
            "El contenido debe ser extenso y completo, con explicaciones profundas y ejemplos cuando corresponda. "
            "El documento debe compilarse sin errores con pdflatex y no debe incluir tabla de contenidos, índices ni texto de ejemplo. "
            "Devuelve únicamente el código LaTeX. "
            "Utiliza un preámbulo moderno, una portada impactante y secciones bien definidas. "
            "Recuerda que los títulos de las secciones no deben llevar numeración. Por ejemplo, en lugar de '2 Estándar ISO/IEC 25010' "
            "y '2.1 Características de la Calidad del Producto', simplemente usa 'Estándar ISO/IEC 25010' y 'Características de la Calidad del Producto'.\n\n"
            "--- Información del Estudiante ---\n"
            f"Nombre: {student_data['nombre']}\n"
            f"C.I.: {student_data['ci']}\n"
            f"Materia: {student_data['materia']}\n"
            f"Sección: {student_data['seccion']}\n"
            f"Universidad: {student_data['universidad']}\n"
            f"Carrera: {student_data['carrera']}\n"
            f"Evaluación: Evaluación N° {student_data['eval_num']} - Corte {student_data['corte']}\n"
            f"Fecha: {student_data['fecha']}\n\n"
            "--- Detalles del Documento ---\n"
            f"Tema: {topic}\n"
            f"Instrucciones específicas: {instructions}\n\n"
            "Requisitos adicionales:\n"
            " - La portada debe incluir el logo de la Universidad. Usa el marcador %%PROJECT_LOGO_PATH%% en el comando de \\includegraphics, "
            "para que luego se reemplace automáticamente por la ruta relativa correcta (recordando que el documento se compila desde la carpeta generated_docs).\n"
            " - No incluir tabla de contenidos ni índices en el documento.\n"
            " - No agregar comentarios o explicaciones adicionales fuera del código LaTeX."
        )
        
        payload = {
            "model": os.getenv("OPENROUTER_MODEL"),
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7
        }

        response = requests.post(API_URL, headers=HEADERS, json=payload)
        response.raise_for_status()

        generated_text = response.json()["choices"][0]["message"]["content"]
        # Reemplazar el marcador por la ruta relativa correcta (desde generated_docs hacia logos)
        generated_text = generated_text.replace("%%PROJECT_LOGO_PATH%%", "../logos/UAH.png")
        logging.info(f"Contenido generado exitosamente. Longitud: {len(generated_text)} caracteres")
        return generated_text

    except requests.exceptions.RequestException as e:
        logging.error(f"Error en la API: {str(e)}")
        raise Exception(f"Error al comunicarse con OpenRouter: {str(e)}")
    except KeyError as e:
        logging.error("Respuesta inesperada de la API")
        raise Exception("La API devolvió una respuesta no válida")
