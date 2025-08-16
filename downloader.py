import yt_dlp
from pathlib import Path
import os
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
        'download_folder': 'descargas',
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


def descargar_mp3(url, config, descargar_playlist=False):
    settings = config['Settings']
    download_folder = settings.get('download_folder', 'descargas')
    audio_quality = settings.get('audio_quality', '192')
    audio_format = settings.get('audio_format', 'mp3')

    dest = Path(__file__).parent / download_folder
    dest.mkdir(parents=True, exist_ok=True)

    opciones = {
        "format": "bestaudio/best",
        "outtmpl": str(dest / "%(title)s.%(ext)s"),
        "writethumbnail": True,
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

    if not descargar_playlist:
        opciones["noplaylist"] = True

    with yt_dlp.YoutubeDL(opciones) as ydl:
        while not terminar:
            try:
                ydl.download([url])
                break
            except Exception as e:
                print(f"Error: {e}")
                if terminar:
                    break


def revisar_descarga(dest, titulo):
    archivos = [f for f in dest.iterdir() if f.is_file()]
    for archivo in archivos:
        if archivo.name.startswith(titulo):
            return True
    return False


if __name__ == "__main__":
    config = get_config()
    settings = config['Settings']
    download_folder = settings.get('download_folder', 'descargas')
    descargas_dir = Path(__file__).parent / download_folder

    link = input("Pega el link de YouTube: ")
    print("¿Qué deseas descargar?")
    print("1. Playlist completo")
    print("2. Solo la canción")
    respuesta = input("Opción: ")

    if respuesta == "1":
        print("\nDescargando playlist completo...")
        descargar_mp3(link, config=config, descargar_playlist=True)
        print(f"✅ Descarga completa. Revisa {str(descargas_dir)}")

    elif respuesta == "2":
        titulo = None
        print("\nObteniendo información del video para evitar duplicados...")
        try:
            ydl_opts = {
                'quiet': True,
                'socket_timeout': 15,  # 15 segundos de tiempo de espera
                'noplaylist': True,    # Asegurarse de procesar solo el video
            }
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(link, download=False)
                titulo = info.get("title", None)
        except Exception as e:
            print(f"No se pudo verificar el título del video (Error: {e}).")
            print("Se procederá a descargar sin verificar duplicados.")

        if titulo and revisar_descarga(descargas_dir, titulo):
            print(f"\nLa canción '{titulo}' ya existe en la carpeta de descarga. No se descargará.")
        else:
            if titulo:
                print(f"'{titulo}' no se encontró en la carpeta. Iniciando descarga...")
            else:
                print("Iniciando descarga...")
            descargar_mp3(link, config=config, descargar_playlist=False)
            print(f"✅ Descarga completa. Revisa {str(descargas_dir)}")

    else:
        print("\nOpción inválida. Saliendo...")
        exit()
