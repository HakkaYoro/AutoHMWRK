import os
import logging
import requests
from bs4 import BeautifulSoup
from PIL import Image
from io import BytesIO
import random
import time

def download_images(query: str, output_dir: str, limit: int = 3) -> list:
    """
    Descarga imágenes relevantes usando DuckDuckGo (versión html/lite) para evitar bloqueos de Google.
    """
    try:
        os.makedirs(output_dir, exist_ok=True)
        image_paths = []
        
        logging.info(f"Buscando imágenes para: {query}")
        
        # Headers para simular navegador real
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }
        
        # Usamos DuckDuckGo HTML que es más fácil de scrapear sin JS
        url = f"https://duckduckgo.com/html/?q={query}"
        
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, "html.parser")
        
        # DuckDuckGo images in HTML mode are usually in 'a.result__a' or similar. 
        # Actually standard HTML DDG disables images sometimes. 
        # Let's try a robust Google selector fallback if we stick to Google, 
        # but the previous error was fetching the google logo.
        
        # New Google Logic:
        # Search URL
        google_url = f"https://www.google.com/search?q={query}&tbm=isch&udm=2" # udm=2 forces "Web" but tbm=isch is images.
        # Adding 'gl=us' or 'hl=es' might help.
        
        response = requests.get(google_url, headers=headers)
        
        # The raw Google HTML for images is messy. It usually hides images in Base64 or separate JSON.
        # Fallback simplistic approach: Look for 'img' tags that have 'src' starting with http 
        # and are NOT the logo.
        
        soup = BeautifulSoup(response.text, "html.parser")
        img_tags = soup.find_all("img")
        
        count = 0
        for img in img_tags:
            if count >= limit:
                break
                
            src = img.get('src')
            if not src:
                src = img.get('data-src')
                
            if src and src.startswith('http') and 'google' not in src and 'gstatic' in src: 
                # gstatic is usually the thumbnails.
                # 'google' in src usually indicates the main logo (www.google.com/...)
                
                try:
                    # Download
                    desc = f"{query}_{count}"
                    path = download_image(src, output_dir, desc)
                    if path:
                        image_paths.append(path)
                        count += 1
                except Exception:
                    continue

        if not image_paths:
             logging.warning("No se encontraron imágenes en el primer intento.")
        
        return image_paths
    
    except Exception as e:
        logging.error(f"Error al descargar imágenes: {str(e)}")
        return []

def download_image(image_url: str, output_dir: str, name_suffix: str) -> str:
    try:
        response = requests.get(image_url, timeout=5)
        response.raise_for_status()
        
        image = Image.open(BytesIO(response.content))
        
        if image.mode in ("P", "RGBA"):
            image = image.convert("RGB")
            
        # Resize if too small (thumbnails)
        if image.width < 50 or image.height < 50:
            return None

        filename = f"img_{name_suffix}.jpg"
        # Sanitize filename
        filename = "".join([c for c in filename if c.isalnum() or c in ('_','.')])
        
        filepath = os.path.join(output_dir, filename)
        image.save(filepath)
        logging.info(f"Imagen guardada: {filepath}")
        return filepath
    except Exception as e:
        # logging.debug(f"Error bajando imagen individual: {e}")
        return None
