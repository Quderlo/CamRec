import pickle
import tkinter as tk
from tkinter import messagebox

import cv2
from PIL import ImageTk, Image

import settings
from encode_and_compare import encode_face, check_duplicate_encodings

from dataBaseConnect import connection


class AddToDatabase(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.recognition_window = parent

        self.return_to_main_menu_btn = tk.Button(self, text="Вернуться в меню",
                                                 command=self.return_to_main_menu)
        self.return_to_main_menu_btn.pack()

        self.cam = None

        self.video_label = tk.Label(self.recognition_window)

        self.take_photo_btn = tk.Button(self, text="Сделать снимок", command=self.take_photo)

        self.image = None
        self.gray = None
        self.faces = None

        self.start_face_recognition_id = None
        self.show_video_id = None
        self.showing_photo = False

        self.retake_photo = tk.Button(self, text="Переснять фото", command=self.retake_photo)
        self.add_to_database_btn = tk.Button(self, text="Добавить в базу", command=self.add_to_database)

    def return_to_main_menu(self):
        self.return_to_main_menu_btn.pack_forget()
        self.recognition_window.go_to_database_frame_btn.pack()
        self.recognition_window.go_to_recognition_frame_btn.pack()
        self.pack_forget()
        self.video_label.pack_forget()
        self.take_photo_btn.pack_forget()
        self.retake_photo.pack_forget()
        self.add_to_database_btn.pack_forget()
        self.showing_photo = False

        if self.start_face_recognition_id is not None:
            self.after_cancel(self.start_face_recognition_id)
        if self.show_video_id is not None:
            self.after_cancel(self.show_video_id)

        self.cam.release()
        cv2.destroyAllWindows()
        self.cam = None

    def get_cursor(self):
        if self.cam is None:
            self.cam = cv2.VideoCapture(settings.cam_port)

        self.return_to_main_menu_btn.pack()
        self.video_label.pack()
        self.take_photo_btn.pack()

        self.recognition_window.cursor.execute("SELECT name, encodings FROM face_encodings")

    def get_faces(self):
        self.image = None
        self.gray = None
        self.faces = None

        result, self.image = self.cam.read()

        try:
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.faces = settings.face_detector(self.gray)
        except cv2.error as e:
            print(f"OpenCV error: {e}. In get_faces_images.")
        except Exception as ex:
            print(f"Error: {ex}. In get_faces_images.")

        self.start_face_recognition_id = self.after(10, self.outline_face)

    def outline_face(self):
        for face in self.faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(self.image, (x, y), (x + w, y + h), settings.face_rectangle_color, 2)

        img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        if not self.showing_photo:
            self.get_faces()

    def add_to_database(self):
        self.retake_photo.pack_forget()
        self.add_to_database_btn.pack_forget()
        self.showing_photo = False

        name = "Lev"

        encodings = encode_face(self.image, self.gray, self.faces)

        # try:
        if len(encodings) > 0:
            byte_data = pickle.dumps(encodings)
            print("Кодировки лиц в байтах:", byte_data)
            print("Лицо найдено")

            if not check_duplicate_encodings(encodings):
                self.recognition_window.cursor.execute(
                    "CREATE TABLE IF NOT EXISTS face_encodings (id SERIAL PRIMARY KEY, name VARCHAR(255), encodings BYTEA)"
                )
                self.recognition_window.cursor.execute(
                    "INSERT INTO face_encodings (name, encodings) VALUES (%s, %s)",
                    (name, byte_data)
                )
                connection.commit()
                messagebox.showinfo(title="Успешно", message=f"Пользователь {name}. Был "
                                                             "зарегистрирован")
            else:
                messagebox.showerror(title="Не удалось добавить в базу", message="Похожий на вас пользователь уже "
                                                                                 "зарегистрирован")
        else:
            messagebox.showerror(title="Не удалось добавить в базу", message="Не обнаружено лицо на кадре")
        # except:
        #     print("Error: Something went wrong at adding in database")

        self.get_faces()

    def take_photo(self):
        self.retake_photo.pack()
        self.add_to_database_btn.pack()
        self.showing_photo = True

    def retake_photo(self):
        self.retake_photo.pack_forget()
        self.add_to_database_btn.pack_forget()
        self.showing_photo = False
        self.get_faces()

    def start_frame(self):
        self.get_faces()