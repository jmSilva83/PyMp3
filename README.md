# Descargador de Audio de YouTube

Este es un programa de Python que te permite descargar audio de videos de YouTube, con una interfaz de línea de comandos y una interfaz gráfica de usuario.

## Características

-   Descarga de videos individuales o playlists completas.
-   Conversión a formato de audio configurable (por defecto, MP3 a 192kbps).
-   Incrusta la carátula del video en el archivo de audio.
-   Evita descargar archivos duplicados que ya existen.
-   Interfaz Gráfica (GUI) para un uso fácil e intuitivo.
-   Selector de carpeta para elegir dónde guardar cada descarga.
-   Barra de progreso y botón para abrir la carpeta de descargas.

## Requisitos

-   Python 3.6 o superior
-   Dependencias de Python listadas en `requirements.txt`
-   `ffmpeg`: una herramienta esencial para la conversión de audio y video.

## Instalación

1.  **Clona o descarga este repositorio.**

2.  **Instala las dependencias de Python:**
    Desde la carpeta del proyecto, ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Instala `ffmpeg`:**
    Sigue las instrucciones de instalación para tu sistema operativo en el [sitio web oficial de ffmpeg](https://ffmpeg.org/download.html) y asegúrate de que esté accesible en el PATH de tu sistema.

## Configuración

La primera vez que ejecutes el script, se creará automáticamente un archivo `config.ini`. Puedes editar este archivo para cambiar:

-   `audio_quality`: La calidad del audio en kbps (por defecto: `192`).
-   `audio_format`: El formato del audio (por defecto: `mp3`).

## Modo de Uso

Puedes usar este programa de dos maneras:

### 1. Versión Gráfica (GUI) - Recomendado

Es la forma más sencilla. Ejecuta el siguiente comando y se abrirá una ventana fácil de usar:
```bash
python gui.py
```
Al presionar "Descargar", se abrirá un explorador de archivos para que elijas dónde guardar el audio. Después de una descarga exitosa, se activará un botón para abrir directamente esa carpeta.

### 2. Línea de Comandos (CLI)

Para usuarios avanzados, la versión de línea de comandos sigue disponible:
```bash
python downloader.py
```
El script te guiará para pegar un link y elegir una opción. Los archivos se guardarán por defecto en una carpeta `descargas`.

## Crear un Ejecutable (Distribución)

Para convertir esta aplicación en un programa de escritorio que puedas compartir (un `.exe` en Windows), sigue estos pasos:

1.  **Instala las dependencias de desarrollo:**
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Ejecuta el script de compilación:**
    Para usuarios de Windows, simplemente haz doble clic en el archivo `build.bat`.

3.  **Encuentra tu aplicación:**
    Una vez que el proceso termine, se creará una carpeta `dist/PyMp3`. Dentro de esta carpeta está tu programa (`PyMp3.exe`) y todos los archivos que necesita.

4.  **Prepara la distribución:**
    Copia el archivo `ffmpeg.exe` (que debes descargar por separado) y pégalo dentro de la carpeta `dist/PyMp3`. Ahora puedes comprimir la carpeta `dist/PyMp3` completa en un archivo ZIP y compartirla.

## Pruebas

Este proyecto incluye pruebas automatizadas. Para ejecutarlas:

1.  **Instala las dependencias de desarrollo:**
    ```bash
    pip install -r requirements-dev.txt
    ```

2.  **Ejecuta las pruebas:**
    Desde la raíz del proyecto, ejecuta el comando correspondiente a tu sistema operativo:
    -   **Linux/macOS:** `PYTHONPATH=. pytest`
    -   **Windows (CMD):** `set PYTHONPATH=.; pytest`
    -   **Windows (PowerShell):** `$env:PYTHONPATH = "."; pytest`

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
