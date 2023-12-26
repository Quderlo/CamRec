import tkinter as tk
import settings
from dataBaseConnect import connection
from face_recognition_frame import FaceRecognition
from add_to_database_frame import AddToDatabase


class RecognitionWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Распознование лиц")
        self.geometry(settings.window_size)
        self.attributes("-topmost", True)
        self.face_recognition_frame = FaceRecognition(self)
        self.database_frame = AddToDatabase(self)

        self.go_to_database_frame_btn = tk.Button(self, text="Добавить лицо в базу",
                                                  command=self.go_to_add_to_database)
        self.go_to_database_frame_btn.pack()

        self.go_to_recognition_frame_btn = tk.Button(self, text="Распознование лиц",
                                                     command=self.go_to_face_recognition)
        self.go_to_recognition_frame_btn.pack()

        self.cursor = connection.cursor()

    def go_to_add_to_database(self):
        self.go_to_database_frame_btn.pack_forget()
        self.go_to_recognition_frame_btn.pack_forget()

        self.database_frame.pack()
        self.database_frame.get_cursor()
        self.database_frame.start_frame()

    def go_to_face_recognition(self):
        self.go_to_database_frame_btn.pack_forget()
        self.go_to_recognition_frame_btn.pack_forget()

        self.face_recognition_frame.pack()
        self.face_recognition_frame.get_cursor()
        self.face_recognition_frame.start_recognition()



