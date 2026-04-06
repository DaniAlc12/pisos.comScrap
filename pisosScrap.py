import asyncio
from urllib.parse import urljoin
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup
import random
import csv
import sys

URL_INICIAL = "https://www.pisos.com/alquiler/pisos-madrid/"
DOMINIO_BASE = "https://www.pisos.com"

async def main():
    limite_input = input("¿Cuántas páginas quieres scrapear? (Escribe 0 para no poner límite): ")
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
            locale="es-ES"
        )
        
        page = await context.new_page()
        
        url_actual = URL_INICIAL
        contador_paginas = 1
        lista_pisos = []  
        
        while True:
            if limite_paginas > 0 and contador_paginas > limite_paginas:
                print(f"\n[INFO] Límite de {limite_paginas} páginas alcanzado. Finalizando navegación.")
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
                elemento_subtitulo = piso.select_one(".ad-preview__subtitle")
                
                if elemento_subtitulo is None:
                    continue
                    
                titulo = elemento_subtitulo.text.strip()
                
                try:
                    elemento_precio = piso.select_one(".ad-preview__price")
                    if elemento_precio:
                        precio = int(
                            elemento_precio.text.strip()
                            .replace("€", "")
                            .replace(".", "")
                            .replace("/mes", "")
                            .strip()
                        )
                    else:
                        precio = 0
                except ValueError:
                    print(f"  [!] Precio con formato desconocido para: {titulo}")
                    precio = 0
                    
                print(f"  -> Capturado: {titulo} | {precio}€")
                lista_pisos.append({"titulo": titulo, "precio": precio})
            
            boton_siguiente = await page.query_selector("span:has-text('Siguiente')")
            
            if boton_siguiente is None:
                print("No hay botón de Siguiente. Fin de la extracción.")
                break
            else:
                href_extraido = await boton_siguiente.evaluate("nodo => nodo.parentElement.getAttribute('href')")
                url_actual = urljoin(DOMINIO_BASE, href_extraido)
            
            await asyncio.sleep(random.uniform(2, 4))
            contador_paginas += 1

        await browser.close()

    print("\nGuardando datos en CSV...")
    if lista_pisos:
        with open("resultados_pisos.csv", "w", newline="", encoding="utf-8") as archivo:
            columnas = ["titulo", "precio"]
            escritor = csv.DictWriter(archivo, fieldnames=columnas)
            escritor.writeheader()
            escritor.writerows(lista_pisos)
        print(f"¡PROCESO FINALIZADO! Total capturados y guardados: {len(lista_pisos)} pisos.")
    else:
        print("No se ha capturado ningún piso. El archivo CSV no se ha generado.")


if __name__ == "__main__":
    asyncio.run(main())