import yt_dlp
from yt_dlp.utils import DownloadError, ExtractorError
from pathlib import Path
import os
import sys
import signal
import configparser

terminar = False


def signal_handler(sig, frame):
    global terminar
    terminar = True


signal.signal(signal.SIGINT, signal_handler)


def crear_config_default(config_path):
    """Crea un archivo de configuración con valores por defecto."""
    config = configparser.ConfigParser()
    config['Settings'] = {
        'audio_quality': '192',
        'audio_format': 'mp3'
    }
    with open(config_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    print(f"Se ha creado un archivo de configuración por defecto en: {config_path}")
    return config

def get_config():
    """Lee la configuración desde config.ini o la crea si no existe."""
    config_path = Path(__file__).parent / "config.ini"
    if not config_path.exists():
        return crear_config_default(config_path)

    config = configparser.ConfigParser()
    config.read(config_path, encoding='utf-8')
    return config


def descargar_mp3(url, config, destination_folder, descargar_playlist=False, progress_hook=None):
    settings = config['Settings']
    audio_quality = settings.get('audio_quality', '192')
    audio_format = settings.get('audio_format', 'mp3')

    dest = Path(destination_folder)
    dest.mkdir(parents=True, exist_ok=True)

    opciones = {
        "format": "bestaudio/best",
        "outtmpl": str(dest / "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "nooverwrites": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": audio_format,
                "preferredquality": audio_quality,
            },
            {
                "key": "EmbedThumbnail",
            },
        ],
    }

    # Auto-detect local ffmpeg when running as a bundled exe
    if getattr(sys, 'frozen', False):
        base_path = Path(sys.executable).parent
        ffmpeg_path = base_path / 'ffmpeg.exe'
        if ffmpeg_path.exists():
            opciones['ffmpeg_location'] = str(ffmpeg_path)

    if not descargar_playlist:
        opciones["noplaylist"] = True

    if progress_hook:
        opciones['progress_hooks'] = [progress_hook]

    with yt_dlp.YoutubeDL(opciones) as ydl:
        while not terminar:
            try:
                ydl.download([url])
                break
            except DownloadError:
                print(f"\n[Error de Descarga] No se pudo bajar el video.")
                print("El video podría no estar disponible en el formato solicitado o puede haber un problema de red.")
                break
            except ExtractorError:
                print(f"\n[Error de Extracción] No se pudo procesar la URL.")
                print("Verifica si la URL es correcta o si el video es privado o restringido.")
                break
            except Exception as e:
                print(f"\n[Error Inesperado] Ocurrió un problema: {e}")
                if terminar:
                    break


def main():
    config = get_config()
    link = input("Pega el link de YouTube: ")
    print("¿Qué deseas descargar?")
    print("1. Playlist completo")
    print("2. Solo la canción")
    respuesta = input("Opción: ")

    if respuesta == "1":
        dest_folder = Path(__file__).parent / "descargas"
        print("\nDescargando playlist completo...")
        descargar_mp3(link, config=config, destination_folder=str(dest_folder), descargar_playlist=True)
        print(f"✅ Descarga completa. Revisa {str(dest_folder)}")

    elif respuesta == "2":
        dest_folder = Path(__file__).parent / "descargas"
        print("\nDescargando canción...")
        descargar_mp3(link, config=config, destination_folder=str(dest_folder), descargar_playlist=False)
        print(f"✅ Descarga completa. Revisa {str(dest_folder)}")

    else:
        print("\nOpción inválida. Saliendo...")
        exit()


if __name__ == "__main__":
    main()
