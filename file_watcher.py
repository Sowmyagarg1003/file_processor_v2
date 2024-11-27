import os
import time

from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

from file_utils import process_file


class Handler(FileSystemEventHandler):
    def on_created(self, event):
        if not event.is_directory:
            process_file(event.src_path)

class Watcher:
    def __init__(self, path='data/'):
        self.observer = Observer()
        self.path = path

    def run(self):
        # Process already existing files in the folder
        self.process_existing_files()

        # Now start watching for new files
        event_handler = Handler()
        self.observer.schedule(event_handler, self.path, recursive=True)
        self.observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            self.observer.stop()
        self.observer.join()

    def process_existing_files(self):
        # Iterate over existing files in the directory
        for filename in os.listdir(self.path):
            file_path = os.path.join(self.path, filename)
            if os.path.isfile(file_path):
                process_file(file_path)
