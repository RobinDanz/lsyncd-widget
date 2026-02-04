
import os
import time
from PyQt6.QtCore import QThread, pyqtSignal
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer


class LogWatcher(QThread):
    """Watches the Lsyncd logfile using watchdog. Runs in a separate thread
    """
    copy_start = pyqtSignal()
    copy_end = pyqtSignal()
    
    def __init__(self, logfile):
        super().__init__()
        self.logfile = logfile
        self._running = True
        
    def run(self):
        class Handler(FileSystemEventHandler):
            def __init__(self, outer):
                super().__init__()
                self.outer = outer
                with open(self.outer.logfile, 'rb') as f:
                    f.seek(0, os.SEEK_END)
                    self._position = f.tell()
                
            def on_modified(self, event):
                if event.src_path != os.path.abspath(self.outer.logfile):
                    return
                
                with open(event.src_path, 'r') as f:
                    f.seek(self._position)
                    new_lines = f.readlines()
                    self._position = f.tell()
                    
                for line in new_lines:
                    self.process_line(line)
                    
            def process_line(self, line):
                if not line:
                    return
                
                if "Normal: Calling rsync" in line:
                    self.outer.copy_start.emit()

                elif "sending incremental file list" in line:
                    self.outer.log_changed.emit('sync_list_start')

                elif "sent" in line and "bytes" in line:
                    self.outer.log_changed.emit('sync_list_end')

                elif "Normal: Finished" in line:
                    self.outer.copy_end.emit()
        
        observer = Observer()
        handler = Handler(self)
        observer.schedule(
            handler, 
            os.path.dirname(os.path.abspath(self.logfile)), 
            recursive=False
        )
        observer.start()
        
        try: 
            while self._running:
                time.sleep(1)
        finally:
            observer.stop()
            observer.join()
            
    def stop(self):
        self._running = False