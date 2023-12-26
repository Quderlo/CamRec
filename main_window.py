import tkinter as tk
import cv2
import settings
from dataBaseConnect import connection
from face_recognition_frame import FaceRecognition


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

    def go_to_face_recognition(self):
        self.go_to_database_frame_btn.pack_forget()
        self.go_to_recognition_frame_btn.pack_forget()

        self.face_recognition_frame.pack()
        self.face_recognition_frame.get_cursor()
        self.face_recognition_frame.start_recognition()


class AddToDatabase(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.recognition_window = parent

        self.return_to_main_menu_btn = tk.Button(self, text="Вернуться в меню",
                                                 command=self.return_to_main_menu)
        self.return_to_main_menu_btn.pack()

        self.cam = cv2.VideoCapture(settings.cam_port)

    def return_to_main_menu(self):
        self.return_to_main_menu_btn.pack_forget()
        self.recognition_window.go_to_database_frame_btn.pack()
        self.recognition_window.go_to_recognition_frame_btn.pack()
        self.pack_forget()


if __name__ == "__main__":
    root = RecognitionWindow()
    root.protocol("WM_DELETE_WINDOW", root.quit)  # Добавьте эту строку для обработки закрытия окна Tk
    root.mainloop()
