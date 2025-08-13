import os
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ReloadHandler(FileSystemEventHandler):
    def __init__(self, command):
        self.command = command
        self.process = subprocess.Popen(self.command, shell=True)

    def on_any_event(self, event):
        print(f"🔁 Cambio detectado en {event.src_path}, reiniciando...")
        self.process.kill()
        time.sleep(0.2)
        self.process = subprocess.Popen(self.command, shell=True)

if __name__ == "__main__":
    command = "python main.py"
    path = "./"  # Carpeta raíz del proyecto

    event_handler = ReloadHandler(command)
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=True)
    observer.start()
    print("👀 Escuchando cambios en el proyecto...")

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        event_handler.process.kill()

    observer.join()
