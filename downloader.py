import yt_dlp
from pathlib import Path
import os
import signal

terminar = False


def signal_handler(sig, frame):
    global terminar
    terminar = True


signal.signal(signal.SIGINT, signal_handler)


def descargar_mp3(url, descargar_playlist=False):
    dest = Path(__file__).parent / "descargas"
    dest.mkdir(parents=True, exist_ok=True)

    opciones = {
        "format": "bestaudio/best",
        "outtmpl": str(dest / "%(title)s.%(ext)s"),
        "writethumbnail": True,
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
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
    link = input("Pega el link de YouTube: ")
    print("¿Qué deseas descargar?")
    print("1. Playlist completo")
    print("2. Solo la canción")
    respuesta = input("Opción: ")

    if respuesta == "1":
        print("\nDescargando playlist completo...")
        descargar_mp3(link, descargar_playlist=True)
        print(f"✅ Descarga completa. Revisa {str(Path(__file__).parent / 'descargas')}")

    elif respuesta == "2":
        descargas_dir = Path(__file__).parent / "descargas"
        descargas_dir.mkdir(parents=True, exist_ok=True)

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
            descargar_mp3(link, descargar_playlist=False)
            print(f"✅ Descarga completa. Revisa {str(descargas_dir)}")

    else:
        print("\nOpción inválida. Saliendo...")
        exit()
