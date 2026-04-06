Utilizar el comando: pip install -r requirements.txt
# Madrid Real Estate Scraper - Pisos.com

Este proyecto es una herramienta de extracción de datos (web scraping) desarrollada en Python para recopilar información sobre el mercado inmobiliario en Madrid desde el portal Pisos.com.

## Objetivo
El propósito de este script es puramente educativo y de análisis de datos. Permite obtener detalles como precio, metros cuadrados, número de habitaciones y ubicación para su posterior procesamiento en análisis estadísticos o visualización de datos.

## Tecnologías utilizadas
* **Python 3.x**
* **Bibliotecas:** `BeautifulSoup4`, `Requests`, `Pandas` (puedes cambiar esto según lo que uses, ej. Selenium o Playwright).

## Aviso Legal (Disclaimer)
Este proyecto ha sido creado con fines exclusivamente académicos y de aprendizaje. 
1. **Uso Responsable:** El autor no se hace responsable del uso indebido de este script. 
2. **Términos de Servicio:** Este script no debe ser utilizado para violar los Términos y Condiciones de Pisos.com. Se recomienda revisar el archivo `robots.txt` del sitio antes de ejecutarlo.
3. **Limitación de Carga:** El script incluye pausas aleatorias (`time.sleep`) para evitar sobrecargar los servidores del portal.

## Características
* Extracción de títulos y descripciones.
* Captura de precios y variaciones.
* Limpieza automática de datos y exportación a formato `.csv` o `.json`.

## Instalación y Uso
1. Clona el repositorio:
   ```bash
   git clone [https://github.com/tu-usuario/madrid-housing-scraper.git](https://github.com/tu-usuario/madrid-housing-scraper.git)