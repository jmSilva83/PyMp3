# Descargador de Audio de YouTube

Este es un sencillo script de Python que te permite descargar audio de videos de YouTube, ya sea una sola canción o una playlist completa. El audio se convierte y guarda en formato MP3.

## Características

- Descarga de videos individuales o playlists completas.
- Convierte el audio a formato MP3 con una calidad de 192 kbps.
- Guarda los archivos en una carpeta `descargas` en el mismo directorio del script.
- Incrusta la carátula del video en el archivo MP3.
- Verifica si una canción ya ha sido descargada para evitar duplicados.
- Manejo de interrupciones con `Ctrl+C` para detener la descarga de forma segura.


## Requisitos

Para utilizar este script, necesitas tener instalado lo siguiente:

- Python 3.6 o superior
- `yt-dlp`: una herramienta de línea de comandos para descargar videos de YouTube y otros sitios.
- `ffmpeg`: una herramienta esencial para la conversión de audio y video.

## Instalación

Sigue estos pasos para preparar tu entorno:

1.  **Clona o descarga este repositorio.**

2.  **Instala las dependencias de Python.**
    Navega hasta el directorio del proyecto en tu terminal y ejecuta:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Instala `ffmpeg`.**
    `ffmpeg` es necesario para la conversión de audio. Debes descargarlo y asegurarte de que esté accesible desde la línea de comandos (es decir, que esté en el PATH de tu sistema).

    -   **En Windows:**
        1.  Descarga `ffmpeg` desde [el sitio oficial](https://ffmpeg.org/download.html).
        2.  Descomprime el archivo en una ubicación de tu preferencia (por ejemplo, `C:\ffmpeg`).
        3.  Añade la carpeta `bin` de `ffmpeg` (ej. `C:\ffmpeg\bin`) a la variable de entorno PATH de tu sistema.

    -   **En macOS (usando Homebrew):**
        ```bash
        brew install ffmpeg
        ```

    -   **En Linux (usando `apt` en sistemas Debian/Ubuntu):**
        ```bash
        sudo apt-get update
        sudo apt-get install ffmpeg
        ```

## Configuración

La primera vez que ejecutes el script, se creará automáticamente un archivo `config.ini` en el mismo directorio. Este archivo te permite personalizar algunas opciones de la descarga.

Puedes editar este archivo para cambiar:

-   `download_folder`: La carpeta donde se guardarán los archivos (por defecto: `descargas`).
-   `audio_quality`: La calidad del audio en kbps (por defecto: `192`).
-   `audio_format`: El formato del audio (por defecto: `mp3`).

## Solución de Problemas

-   **[Error de Extracción]**: Este error suele ocurrir si la URL de YouTube es incorrecta, el video ha sido eliminado, o es privado. Verifica el link que estás usando.
-   **[Error de Descarga]**: Aparece si hay un problema al bajar el archivo. Puede ser un problema temporal de red o que el video no esté disponible en el formato de audio solicitado. Intenta de nuevo más tarde.
-   **`ffprobe and ffmpeg not found`**: Este error de `yt-dlp` significa que `ffmpeg` no está instalado o no es accesible desde el PATH de tu sistema. Sigue las instrucciones de la sección "Instalación" para configurarlo correctamente.

## Modo de Uso

Una vez que hayas completado la instalación, puedes ejecutar el script desde tu terminal:

```bash
python downloader.py
```

El script te pedirá que sigas estos pasos:

1.  **Pega el link de YouTube:** Introduce la URL del video o de la playlist que quieres descargar.
2.  **Elige una opción:**
    -   `1`: Para descargar la playlist completa.
    -   `2`: Para descargar solo la canción/video individual.

Los archivos MP3 descargados se guardarán en la carpeta que hayas configurado en `config.ini`.

### Versión Gráfica (GUI)

Si prefieres una interfaz visual, puedes ejecutar la versión gráfica del programa:

```bash
python gui.py
```

Esto abrirá una ventana donde podrás pegar la URL y seleccionar tus opciones de descarga. Después de una descarga exitosa, se activará un botón para abrir directamente la carpeta de descargas.

## Pruebas

Este proyecto incluye una suite de pruebas automatizadas para asegurar su correcto funcionamiento. Para ejecutar las pruebas, primero necesitas instalar las dependencias de desarrollo:

```bash
pip install -r requirements-dev.txt
```

Luego, puedes ejecutar las pruebas desde la raíz del repositorio.

**En Linux o macOS:**
```bash
PYTHONPATH=. pytest
```

**En Windows (PowerShell):**
```powershell
$env:PYTHONPATH = "."; pytest
```

**En Windows (CMD):**
```cmd
set PYTHONPATH=.; pytest
```

## Licencia

Este proyecto está bajo la Licencia MIT. Consulta el archivo `LICENSE` para más detalles.
