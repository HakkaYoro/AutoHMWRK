import os
import logging
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO

def download_images(text: str, output_dir: str) -> list:
    """
    Descarga imágenes relevantes de Google Images basándose en el texto proporcionado.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        image_paths = []
        
        # Extraer palabras clave del texto
        keywords = extract_keywords(text)
        
        for keyword in keywords:
            # Buscar imágenes en Google Images
            image_url = search_google_images(keyword)
            
            if image_url:
                # Descargar la imagen
                image_path = download_image(image_url, output_dir, keyword)
                if image_path:
                    image_paths.append(image_path)
        
        return image_paths
    
    except Exception as e:
        logging.error(f"Error al descargar imágenes: {str(e)}")
        return []

def extract_keywords(text: str) -> list:
    """
    Extrae palabras clave del texto proporcionado.
    """
    # Implementar lógica para extraer palabras clave relevantes
    # Esto podría incluir el uso de NLP o simplemente dividir el texto en palabras
    # y filtrar las palabras más comunes.
    # Por ahora, simplemente dividiremos el texto en palabras y eliminaremos las palabras comunes.
    stop_words = set(["de", "la", "el", "en", "y", "a", "para", "con", "por", "un", "una", "los", "las"])
    words = text.lower().split()
    keywords = [word for word in words if word not in stop_words]
    return keywords[:5]  # Limitar a las 5 primeras palabras clave

def search_google_images(keyword: str) -> str:
    """
    Busca una imagen en Google Images basándose en la palabra clave proporcionada.
    """
    try:
        url = f"https://www.google.com/search?q={keyword}&tbm=isch"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
        }
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")
        
        if img_tags:
            # Devolver la URL de la primera imagen
            image_url = img_tags[0]["src"]
            if image_url.startswith("/"):
                image_url = "https://www.google.com" + image_url
            return image_url
        else:
            return None
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al buscar imágenes en Google: {str(e)}")
        return None

def download_image(image_url: str, output_dir: str, keyword: str) -> str:
    """
    Descarga una imagen de la URL proporcionada y la guarda en el directorio de salida.
    """
    try:
        response = requests.get(image_url, stream=True)
        response.raise_for_status()
        
        # Abrir la imagen
        image = Image.open(BytesIO(response.content))
        
        # Convertir a RGB si es necesario
        if image.mode == "P":
            image = image.convert("RGB")
        
        # Guardar la imagen en el directorio de salida
        filename = f"{keyword.replace(' ', '_')}.jpg"
        filepath = os.path.join(output_dir, filename)
        image.save(filepath)
        
        logging.info(f"Imagen descargada: {filepath}")
        return filepath
    except requests.exceptions.RequestException as e:
        logging.error(f"Error al descargar la imagen: {str(e)}")
        return None
    except Exception as e:
        logging.error(f"Error al procesar la imagen: {str(e)}")
        return None
