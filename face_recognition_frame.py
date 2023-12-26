import pickle
import tkinter as tk
from PIL import Image, ImageTk
import cv2

import settings
from encode_and_compare import encode_face, compare_encodings


class FaceRecognition(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.recognition_window = parent

        self.return_to_main_menu_btn = tk.Button(self, text="Вернуться в меню",
                                                 command=self.return_to_main_menu)
        self.return_to_main_menu_btn.pack()

        self.cam = None

        self.video_label = tk.Label(self.recognition_window)

        self.image = None
        self.gray = None
        self.faces = None

        self.start_face_recognition_id = None
        self.show_video_id = None

    def return_to_main_menu(self):
        self.return_to_main_menu_btn.pack_forget()
        self.recognition_window.go_to_database_frame_btn.pack()
        self.recognition_window.go_to_recognition_frame_btn.pack()
        self.pack_forget()
        self.video_label.pack_forget()

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

        self.video_label.pack()

        self.recognition_window.cursor.execute("SELECT name, encodings FROM face_encodings")

    def get_faces(self):
        self.image = None
        self.gray = None
        self.faces = None

        result, self.image = self.cam.read()

        try:
            self.gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            self.faces = settings.face_detector(self.gray)

        except:
            print("Error: No image detected. In get_faces_images.")

        self.start_face_recognition_id = self.after(100, self.start_face_recognition)

    def start_face_recognition(self):

        encodings = []

        rows = None

        try:
            rows = self.recognition_window.cursor.fetchall()
        except:
            print("Error: Cant fetch faces from database. In start_face_recognition")

        try:
            for face in self.faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(self.image, (x, y), (x + w, y + h), settings.face_rectangle_color, 2)

                encodings.append(encode_face(self.image, self.gray, face))

                found_match = False
                name = None
                for row in rows:
                    db_encodings = pickle.loads(row[1])
                    if compare_encodings(encodings, db_encodings):
                        name = row[0]
                        found_match = True
                        break

                if found_match and name:
                    cv2.putText(self.image, name, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                elif len(encodings) >= 0:
                    cv2.putText(self.image, "Neznakomec", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255),
                                2)
        except: print("Can't put Text in image")

        # self.show_video_id = self.after(100, self.show_video)
        try:
            img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
            imgtk = ImageTk.PhotoImage(image=img)

            self.video_label.imgtk = imgtk
            self.video_label.configure(image=imgtk)
        except: print("Error: Can't display image or image is not found. In start_face_recognition")

        self.get_faces()

    # def show_video(self):
    #     img = Image.fromarray(cv2.cvtColor(self.image, cv2.COLOR_BGR2RGB))
    #     imgtk = ImageTk.PhotoImage(image=img)
    #
    #     self.video_label.imgtk = imgtk
    #     self.video_label.configure(image=imgtk)
    #
    #     self.get_faces()

    def start_recognition(self):
        self.get_faces()
