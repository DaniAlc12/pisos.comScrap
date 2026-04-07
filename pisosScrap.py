import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import sys
import sqlite3
import re

URL_INICIAL = "https://www.pisos.com/alquiler/pisos-madrid/"
DOMINIO_BASE = "https://www.pisos.com"


async def main():
    limite_input = input(
        "¿Cuántas páginas quieres scrapear? (Escribe 0 para no poner límite): "
    )
    try:
        limite_paginas = int(limite_input)
    except ValueError:
        print("Error: Debes introducir un número. Abortando ejecución por seguridad.")
        sys.exit(1)

    async with async_playwright() as p:

        browser = await p.chromium.launch(headless=True)

        context = await browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            viewport={"width": 1920, "height": 1080},
            locale="es-ES",
        )

        page = await context.new_page()

        #Así se hace la entrada dinámica limpia:
        zona_input = (
            input(
                "¿Qué localidad/zona quieres buscar? (ej: madrid, barcelona, valencia): "
            )
            .strip()
            .lower()
            .replace(" ", "-")
        )
        url_actual = f"https://www.pisos.com/alquiler/pisos-{zona_input}/"
        contador_paginas = 1
        lista_pisos = []

        while True:
            if limite_paginas > 0 and contador_paginas > limite_paginas:
                print(
                    f"\n[INFO] Límite de {limite_paginas} páginas alcanzado. Finalizando navegación."
                )
                break

            print(f"\n--- Scrapeando página {contador_paginas} ---")
            print(f"URL: {url_actual}")

            await page.goto(url_actual)

            try:
                await page.click("button:has-text('Aceptar y cerrar')", timeout=3000)
                print("Banner de cookies cerrado.")
                await asyncio.sleep(1)
            except Exception:
                pass

            await page.wait_for_selector(".ad-preview__info")
            print("Extrayendo datos de la página...")
            contenido_html = await page.content()
            soup = BeautifulSoup(contenido_html, "html.parser")

            pisos = soup.select(".ad-preview__info")
            print(f"[DEBUG] Contenedores de pisos detectados por BS4: {len(pisos)}")

            for piso in pisos:
                # 1.TÍTULO Y UBICACIÓN
                elemento_titulo = piso.select_one(".ad-preview__title")
                elemento_ubi = piso.select_one(".ad-preview__subtitle")

                #CLÁUSULA DE GUARDA: Si no hay ni título ni ubicación, es publicidad
                if not elemento_titulo and not elemento_ubi:
                    continue

                titulo = (
                    elemento_titulo.text.strip() if elemento_titulo else "Sin título"
                )
                ubicacion = (
                    elemento_ubi.text.strip() if elemento_ubi else "Sin ubicación"
                )

                # 2.DESCRIPCIÓN
                elemento_desc = piso.select_one(".ad-preview__description")
                descripcion = (
                    elemento_desc.text.strip() if elemento_desc else "Sin descripción"
                )

                # 3.PRECIO
                try:
                    elemento_precio = piso.select_one(".ad-preview__price")
                    precio = (
                        int(
                            elemento_precio.text.strip()
                            .replace("€", "")
                            .replace(".", "")
                            .replace("/mes", "")
                            .strip()
                        )
                        if elemento_precio
                        else 0
                    )
                except ValueError:
                    precio = 0

                # 4.CARACTERÍSTICAS DINÁMICAS (m2, habs, baños)
                caracteristicas = piso.select(".ad-preview__char")
                m2, habs, banos = "0", "0", "0" 
                
                for char in caracteristicas:
                    texto = char.text.strip().lower()
                    
                    solo_numeros = re.sub(r"\D", "", texto)
                    
                    if not solo_numeros:
                        solo_numeros = "0"
                        
                    if "m²" in texto or "metros" in texto:
                        m2 = solo_numeros
                    elif "hab" in texto:
                        habs = solo_numeros
                    elif "baño" in texto or "aseo" in texto: 
                        banos = solo_numeros

                print(
                    f"  -> Capturado: {titulo} | {ubicacion} | {precio}€ | {m2}m² | {habs} hab | {banos} ba"
                )

                # 5.GUARDADO EN DICCIONARIO
                lista_pisos.append(
                    {
                        "titulo": titulo,
                        "ubicacion": ubicacion,
                        "precio": precio,
                        "m2": m2,
                        "habitaciones": habs,
                        "banos": banos,
                        "descripcion": descripcion,
                    }
                )

            boton_siguiente = await page.query_selector("span:has-text('Siguiente')")

            if boton_siguiente is None:
                print("No hay botón de Siguiente. Fin de la extracción.")
                break
            else:
                href_extraido = await boton_siguiente.evaluate(
                    "nodo => nodo.parentElement.getAttribute('href')"
                )
                url_actual = urljoin(DOMINIO_BASE, href_extraido)

            await asyncio.sleep(random.uniform(2, 4))
            contador_paginas += 1

        await browser.close()

    # 3.GUARDADO EN BASE DE DATOS SQLITE
    print("\nGuardando datos en SQLite...")
    if lista_pisos:
        conexion = sqlite3.connect("inmobiliaria.db")
        cursor = conexion.cursor()

        cursor.execute('''
            CREATE TABLE IF NOT EXISTS pisos (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titulo TEXT,
                ubicacion TEXT,
                precio INTEGER,
                m2 INTEGER,
                habitaciones INTEGER,
                banos INTEGER,
                descripcion TEXT
            )
        ''')

        for piso in lista_pisos:
            cursor.execute('''
                INSERT INTO pisos (titulo, ubicacion, precio, m2, habitaciones, banos, descripcion)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                piso["titulo"], 
                piso["ubicacion"], 
                piso["precio"], 
                int(piso["m2"]), 
                int(piso["habitaciones"]), 
                int(piso["banos"]), 
                piso["descripcion"]
            ))

        conexion.commit()
        conexion.close()

        print(f"¡PROCESO FINALIZADO! Total guardados en BD: {len(lista_pisos)} pisos.")
    else:
        print("No se ha capturado ningún piso. La base de datos no se ha alterado.")


if __name__ == "__main__":
    asyncio.run(main())
