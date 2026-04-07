import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import sys
import sqlite3
import re

# Constantes globales
DOMINIO_BASE = "https://www.pisos.com"

def configurar_busqueda():
    limite_input = input(
        "¿Cuántas páginas quieres scrapear? (Escribe 0 para no poner límite): "
    )
    try:
        limite_paginas = int(limite_input)
    except ValueError:
        print("Error: Debes introducir un número. Abortando ejecución por seguridad.")
        sys.exit(1)

    zona_input = (
        input("¿Qué localidad/zona quieres buscar? (ej: madrid, barcelona, valencia): ")
        .strip()
        .lower()
        .replace(" ", "-")
    )
    url_inicial = f"https://www.pisos.com/alquiler/pisos-{zona_input}/"
    
    return limite_paginas, url_inicial

async def extraer_pisos(url_inicial, limite_paginas):
    lista_pisos = []
    
    # AQUÍ PONEMOS LA P: Dentro del context manager de Playwright
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="es-ES",
        )
        page = await context.new_page()

        url_actual = url_inicial
        contador_paginas = 1

        while True:
            if limite_paginas > 0 and contador_paginas > limite_paginas:
                print(f"\n[INFO] Límite de {limite_paginas} páginas alcanzado.")
                break

            print(f"\n--- Scrapeando página {contador_paginas} ---")
            print(f"URL: {url_actual}")

            await page.goto(url_actual)

            try:
                # Gestionar cookies
                await page.click("button:has-text('Aceptar y cerrar')", timeout=3000)
                await asyncio.sleep(1)
            except Exception:
                pass

            await page.wait_for_selector(".ad-preview__info")
            contenido_html = await page.content()
            soup = BeautifulSoup(contenido_html, "html.parser")
            pisos = soup.select(".ad-preview__info")

            for piso in pisos:
                elemento_titulo = piso.select_one(".ad-preview__title")
                elemento_ubi = piso.select_one(".ad-preview__subtitle")
                
                if not elemento_titulo:
                    continue
                
                titulo = elemento_titulo.text.strip()
                ubicacion = elemento_ubi.text.strip() if elemento_ubi else "Sin ubicación"
                
                ruta_enlace = elemento_titulo.get("href")
                if ruta_enlace:
                    enlace = urljoin(DOMINIO_BASE, ruta_enlace)
                else:
                    continue

                elemento_desc = piso.select_one(".ad-preview__description")
                descripcion = elemento_desc.text.strip() if elemento_desc else "Sin descripción"

                try:
                    elemento_precio = piso.select_one(".ad-preview__price")
                    precio = int(re.sub(r"\D", "", elemento_precio.text)) if elemento_precio else 0
                except ValueError:
                    precio = 0

                caracteristicas = piso.select(".ad-preview__char")
                m2, habs, banos = "0", "0", "0" 
                for char in caracteristicas:
                    texto = char.text.strip().lower()
                    solo_numeros = re.sub(r"\D", "", texto) or "0"
                    if "m²" in texto or "metros" in texto:
                        m2 = solo_numeros
                    elif "hab" in texto:
                        habs = solo_numeros
                    elif "baño" in texto or "aseo" in texto: 
                        banos = solo_numeros

                lista_pisos.append({
                    "enlace": enlace,
                    "titulo": titulo, 
                    "ubicacion": ubicacion,
                    "precio": precio,
                    "m2": m2,
                    "habitaciones": habs,
                    "banos": banos,
                    "descripcion": descripcion
                })

            # Paginación
            boton_siguiente = await page.query_selector("span:has-text('Siguiente')")
            if boton_siguiente is None:
                break
            else:
                href_extraido = await boton_siguiente.evaluate("nodo => nodo.parentElement.getAttribute('href')")
                url_actual = urljoin(DOMINIO_BASE, href_extraido)

            await asyncio.sleep(random.uniform(2, 4))
            contador_paginas += 1

        await browser.close()
    return lista_pisos

def guardar_en_sqlite(lista_pisos):
    print("\nGuardando datos en SQLite...")
    conexion = sqlite3.connect("inmobiliaria.db")
    cursor = conexion.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS pisos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                enlace TEXT UNIQUE,
                titulo TEXT,
                ubicacion TEXT,
                precio INTEGER,
                m2 INTEGER,
                habitaciones INTEGER,
                banos INTEGER,
                descripcion TEXT,
                fecha_extraccion DATETIME DEFAULT CURRENT_TIMESTAMP -- Se rellena sola
            )
        ''')
    for piso in lista_pisos:
        cursor.execute('''
            INSERT OR IGNORE INTO pisos (enlace, titulo, ubicacion, precio, m2, habitaciones, banos, descripcion, fecha_extraccion)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, CURRENT_TIMESTAMP)
        ''', (piso["enlace"], piso["titulo"], piso["ubicacion"], piso["precio"], 
              int(piso["m2"]), int(piso["habitaciones"]), int(piso["banos"]), piso["descripcion"]))
    conexion.commit()
    conexion.close()
    print(f"¡Hecho! Total en BD: {len(lista_pisos)} registros procesados.")

async def main():
    limite, url = configurar_busqueda()
    pisos_extraidos = await extraer_pisos(url, limite)
    if pisos_extraidos:
        guardar_en_sqlite(pisos_extraidos)

if __name__ == "__main__":
    asyncio.run(main())