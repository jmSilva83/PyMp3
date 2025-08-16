import yt_dlp
from pathlib import Path
import os
import signal

os.environ["PATH"] += ";C:\\ffmpeg\\bin"

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
        "postprocessors": [
            {
                "key": "FFmpegExtractAudio",
                "preferredcodec": "mp3",
                "preferredquality": "192",
            }
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
        print("Descargando playlist completo...")
        descargar_mp3(link, descargar_playlist=True)
    elif respuesta == "2":
        print("Descargando solo la canción...")
        if revisar_descarga(Path(__file__).parent / "descargas", "titulo_tema"):
            print(f"La canción ya existe en la carpeta de descarga. No se descargará.")
        else:
            descargar_mp3(link, descargar_playlist=False)
    else:
        print("Opción inválida. Saliendo...")
        exit()
    print(f"✅ Descarga completa. Revisa {str(Path(__file__).parent / 'descargas')}")
