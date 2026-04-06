import requests
from bs4 import BeautifulSoup
import time
import random

cabeceras = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/146.0.0.0 Safari/537.36",
    "Accept-Language": "es-ES,es;q=0.9",
    "Referer": "https://www.google.com/"
}

url_actual = "https://www.pisos.com/alquiler/pisos-madrid/"
dominio_base = "https://www.pisos.com"

while True:
    print(f"Scrapeando: {url_actual}")
    
    # 1. PETICIÓN: Haz la petición GET a 'url_actual' usando las 'cabeceras'.
    # Escribe el código aquí:
    
    # 2. PARSEO: Convierte el texto de la respuesta en un objeto BeautifulSoup.
    # Escribe el código aquí:
    

    # --- AQUI IRÁ LA FASE 3 DE EXTRACCIÓN DE PISOS (Lo integraremos después) ---


    # --- FASE 2: NAVEGACIÓN Y CONDICIÓN DE PARADA ---
    # 3. Busca la etiqueta <a> del botón "Siguiente" usando tu selector.
    boton_siguiente = # Escribe el código aquí
    
    # 4. LÓGICA DE TRANSICIÓN:
    if boton_siguiente is None:
        print("No hay más páginas. Saliendo del bucle.")
        break
    else:
        # Extrae el enlace del botón. 
        # RECUERDA MI AVISO: Si el href es relativo (ej: /alquiler/pisos-madrid/2/), 
        # ¿cómo construyes la URL absoluta correcta para la siguiente iteración?
        url_actual = # Escribe el código aquí

    # 5. EVASIÓN TÁCTICA: En tu stack mencionaste el uso de sleep y random.
    # Mete una pausa caótica de entre 2 y 4 segundos antes de la siguiente vuelta.
    # Escribe el código aquí: