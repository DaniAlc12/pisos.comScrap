# Pisos.com Scraper (Async Playwright)

Este script de Python permite extraer información detallada sobre alquileres de viviendas desde el portal **pisos.com**. Utiliza una arquitectura asíncrona para maximizar la eficiencia y herramientas modernas de automatización web para gestionar contenido dinámico, cookies y evitar bloqueos.

## Estructura del Proyecto

Para asegurar el correcto funcionamiento, organiza tus archivos de la siguiente manera:

```text
pisos-scraper/
├── venv/                  # Entorno virtual (se crea al instalar)
├── pisosScrap.py          # Script principal con el código de scraping
├── resultados_pisos.csv   # Archivo generado automáticamente tras la ejecución
└── README.md              # Este archivo de documentación

Características Principales
Búsqueda Dinámica: El script es interactivo; solicita al usuario la ciudad (ej: Madrid, Barcelona) y el número de páginas a procesar.

Navegación Asíncrona: Implementado con Playwright para gestionar esperas de carga y contenido generado por JavaScript.

Limpieza de Datos: Procesa automáticamente precios (convirtiéndolos a enteros), metros cuadrados, habitaciones y baños.

Gestión de Cookies: Incluye una lógica específica para detectar y cerrar el banner de privacidad de la web de forma automática.

Exportación a CSV: Los datos se guardan en un archivo resultados_pisos.csv con codificación UTF-8 para evitar errores de caracteres especiales.

Requisitos e Instalación
1. Requisitos previos
Python 3.8 o superior.

Gestor de paquetes pip.

2. Configuración del entorno
Ejecuta los siguientes comandos en tu terminal dentro de la carpeta del proyecto:

Bash
# Crear entorno virtual
python -m venv venv

# Activar entorno (Windows)
.\venv\Scripts\activate

# Activar entorno (Linux/Mac)
source venv/bin/activate

# Instalar librerías necesarias
pip install playwright beautifulsoup4

# Instalar los navegadores de Playwright
playwright install chromium

Modo de Uso
Una vez configurado, lanza el scraper con el siguiente comando:

python pisosScrap.py

Durante la ejecución, el script te pedirá:

Límite de páginas: Un número entero (ej. 3). Introduce 0 si quieres extraer todos los resultados disponibles en la web.

Zona de búsqueda: El nombre de la localidad (ej. madrid, valencia, sevilla). El script generará la URL correspondiente automáticamente.

Estructura de los Datos Extraídos
El archivo resultados_pisos.csv generado contiene las siguientes columnas:

Columna	Descripción
titulo	Título del anuncio publicado en la web.
ubicacion	Zona, barrio o calle específica del inmueble.
precio	Valor numérico mensual (limpio de símbolos € o puntos).
m2	Superficie en metros cuadrados.
habitaciones	Número de dormitorios.
banos	Número de cuartos de baño.
descripcion	Fragmento del texto descriptivo del anuncio.

⚠️ Aviso Legal e Importante (Warning)
Este proyecto tiene fines estrictamente educativos.

Ética de Scraping: No utilices este script para realizar peticiones masivas que puedan degradar el rendimiento del servicio de pisos.com.

Términos de Servicio: El scraping de datos puede estar restringido por los términos y condiciones del portal. Es responsabilidad exclusiva del usuario cumplir con la legalidad vigente.

Uso de Datos: Los datos obtenidos son para uso personal/investigación. No los utilices para fines comerciales sin permiso.

Responsabilidad: El autor no se hace responsable del uso indebido de esta herramienta ni de posibles bloqueos de IP por parte del servidor.

Desarrollado con ❤️ para la comunidad de Python.