import tkinter as tk
from tkinter import ttk, scrolledtext, filedialog
import threading
import downloader
import queue
import os
import sys
import subprocess

class DownloaderApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Descargador de Audio de YouTube")
        self.root.geometry("600x450")
        self.root.resizable(False, False)

        self.progress_queue = queue.Queue()
        self.last_download_path = None

        # Style
        style = ttk.Style(self.root)
        style.configure("Ready.TButton", foreground="green", font=("TkDefaultFont", 10, "bold"))

        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # --- URL Section ---
        url_frame = ttk.LabelFrame(main_frame, text="URL de YouTube", padding="10")
        url_frame.pack(fill=tk.X, pady=5)

        self.url_var = tk.StringVar()
        self.url_var.trace_add("write", self.update_download_button_state)
        self.url_entry = ttk.Entry(url_frame, width=60, textvariable=self.url_var)
        self.url_entry.pack(fill=tk.X, expand=True)
        self.url_entry.focus()

        # --- Options Section ---
        options_frame = ttk.Frame(main_frame, padding="5")
        options_frame.pack(fill=tk.X)

        self.download_type = tk.StringVar(value="video")

        ttk.Radiobutton(options_frame, text="Descargar solo canción", variable=self.download_type, value="video").pack(side=tk.LEFT, padx=10)
        ttk.Radiobutton(options_frame, text="Descargar playlist", variable=self.download_type, value="playlist").pack(side=tk.LEFT, padx=10)

        # --- Action Buttons ---
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=10)

        self.download_button = ttk.Button(action_frame, text="Descargar", command=self.start_download, state="disabled")
        self.download_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(0, 5))

        self.open_folder_button = ttk.Button(action_frame, text="Abrir Carpeta de Descargas", command=self.open_download_folder, state="disabled")
        self.open_folder_button.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=(5, 0))

        # --- Progress Bar ---
        progress_frame = ttk.LabelFrame(main_frame, text="Progreso", padding="10")
        progress_frame.pack(fill=tk.X, pady=5)

        self.progress_bar = ttk.Progressbar(progress_frame, orient="horizontal", length=100, mode="determinate")
        self.progress_bar.pack(fill=tk.X, expand=True)

        # --- Status Area ---
        status_frame = ttk.LabelFrame(main_frame, text="Estado", padding="10")
        status_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.status_text = scrolledtext.ScrolledText(status_frame, wrap=tk.WORD, height=10, state="disabled")
        self.status_text.pack(fill=tk.BOTH, expand=True)

    def progress_hook(self, d):
        self.progress_queue.put(d)

    def process_queue(self):
        try:
            while True:
                data = self.progress_queue.get_nowait()
                if data['status'] == 'downloading':
                    total_bytes = data.get('total_bytes') or data.get('total_bytes_estimate')
                    if total_bytes:
                        percentage = (data['downloaded_bytes'] / total_bytes) * 100
                        self.progress_bar['value'] = percentage
                        # self.log(f"Descargando: {percentage:.2f}%") # Optional: log percentage
                elif data['status'] == 'finished':
                    self.progress_bar['value'] = 100
                    self.log("Procesando archivo... (puede tardar un momento)")
                self.root.update_idletasks()
        except queue.Empty:
            self.root.after(100, self.process_queue)

    def start_download(self):
        url = self.url_var.get()
        if not url:
            self.log("Por favor, introduce una URL de YouTube.")
            return

        destination_folder = filedialog.askdirectory(title="Selecciona una carpeta para guardar el audio")
        if not destination_folder:
            self.log("Descarga cancelada. No se seleccionó ninguna carpeta.")
            return

        self.download_button.config(state="disabled")
        self.progress_bar['value'] = 0
        self.log("Iniciando descarga...")

        # Run the download in a separate thread
        thread = threading.Thread(target=self.download_worker, args=(url, destination_folder))
        thread.daemon = True
        thread.start()

        # Start processing the queue for progress updates
        self.process_queue()

    def download_worker(self, url, destination_folder):
        try:
            is_playlist = self.download_type.get() == "playlist"
            config = downloader.get_config()

            # Pass the progress hook to the download function
            hook = self.progress_hook

            if is_playlist:
                self.log("Descargando playlist completa...")
                downloader.descargar_mp3(url, config=config, destination_folder=destination_folder, descargar_playlist=True, progress_hook=hook)
            else:
                self.log("Descargando canción...")
                downloader.descargar_mp3(url, config=config, destination_folder=destination_folder, descargar_playlist=False, progress_hook=hook)

            if not self.progress_bar['value'] == 100:
                 self.progress_queue.put({'status': 'finished'})

            self.last_download_path = destination_folder
            self.log("✅ ¡Descarga completa!")
            self.root.after(0, self.enable_open_folder_button)

        except Exception as e:
            self.log(f"[ERROR] Ocurrió un error: {e}")
            self.progress_bar['value'] = 0
        finally:
            self.download_button.config(state="normal")

    def enable_open_folder_button(self):
        self.open_folder_button.config(state="normal", style="Ready.TButton")

    def update_download_button_state(self, *args):
        if self.url_var.get():
            self.download_button.config(state="normal", style="Ready.TButton")
        else:
            self.download_button.config(state="disabled", style="TButton")

    def log(self, message):
        self.status_text.config(state="normal")
        self.status_text.insert(tk.END, message + "\n")
        self.status_text.config(state="disabled")
        self.status_text.see(tk.END)

    def open_download_folder(self):
        if not self.last_download_path:
            self.log("Aún no se ha completado ninguna descarga en esta sesión.")
            return

        path = downloader.Path(self.last_download_path)
        try:
            if not path.is_dir():
                self.log(f"Error: La carpeta de descargas '{path}' no existe.")
                return

            if sys.platform == "win32":
                os.startfile(path)
            elif sys.platform == "darwin": # macOS
                subprocess.Popen(["open", path])
            else: # Linux and other UNIX-like
                subprocess.Popen(["xdg-open", path])
        except Exception as e:
            self.log(f"Error al abrir la carpeta: {e}")

if __name__ == "__main__":
    app_root = tk.Tk()
    app = DownloaderApp(app_root)
    app_root.mainloop()
