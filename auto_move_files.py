from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime
import time
import mimetypes
import os
import random

mimetypes.init()

class MoveFilesHandler(FileSystemEventHandler):
    def process_files(self, file, src, file_extension):
        file_mime_start = mimetypes.guess_type(file)[0]
        new_destination = ""

        if file_mime_start != None:
            file_mime_start = file_mime_start.split('/')[0]

            if file_mime_start in image_mime_ext_types or file_extension in image_mime_ext_types:
                new_destination = images_destionation_folder
            if file_mime_start in audio_mime_ext_types or file_extension in audio_mime_ext_types:
                new_destination = audio_destionation_folder
            if file_mime_start in video_mime_ext_types or file_extension in video_mime_ext_types:
                new_destination = video_destionation_folder
            if file_mime_start in doc_mime_ext_types or file_extension in doc_mime_ext_types:
                new_destination = doc_destionation_folder

        if new_destination != "":
            new_destination = new_destination + "/" + file
            try:
                os.rename(src, new_destination)
            except FileExistsError:
                filename, file_extension = os.path.splitext(new_destination)
                new_destination = filename + "_"+ str(random.randint(1, 100) ) + file_extension
                os.rename(src, new_destination)


    def on_modified(self, event):
        for root, dirs, files in os.walk(folder_to_watch, topdown=False):

            for file in files:
                filename, file_extension = os.path.splitext(file)
                src = root + "/" + file
                self.process_files(file, src, file_extension)


            for dir_name in dirs:
                for file in os.listdir(root):
                    filename, file_extension = os.path.splitext(file)
                    src = root + file
                    self.process_files(file, src, file_extension)




folder_to_watch = "C:\\Users\\Jesmine\\Downloads"
images_destionation_folder = "C:\\Users\\Jesmine\\Pictures"
audio_destionation_folder = "C:\\Users\\Jesmine\\Music"
video_destionation_folder = "C:\\Users\\Jesmine\\Videos"
doc_destionation_folder = "C:\\Users\\Jesmine\\Documents"

image_mime_ext_types = ['image', '.png', '.jpg', 'jpeg']
audio_mime_ext_types = ['audio', '.mp3']
video_mime_ext_types = ['video', '.mp4']
doc_mime_ext_types = ['text', '.pdf', '.docx', '.doc', '.ods', '.xlsx', '.xlsm']

move_files_handler = MoveFilesHandler()
observer = Observer()
observer.schedule(move_files_handler, folder_to_watch, recursive=True)
observer.start()


try:
    while True:
        time.sleep(10)
except KeyboardInterrupt:
    observer.stop()
observer.join()
