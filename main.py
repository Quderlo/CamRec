import tkinter as tk
from addToDataBaseUI import start_camera, add_to_db
import cv2
from settings import cam_port
from face_recognition import show_face_recognition

def retake_camera_photo():
    back_to_menu_from_database()
    go_to_add_to_database()


def adding_to_db():
    add_to_db(cam, name_entry)
    retake_photo_btn.pack()


def back_to_menu_from_database():
    database_window_btn.configure(text="Добавить себя в базу", command=go_to_add_to_database)

    video_label.pack_forget()
    add_to_database_btn.pack_forget()
    retake_photo_btn.pack_forget()
    name_label.pack_forget()
    name_entry.pack_forget()

    cam.release()
    cv2.destroyAllWindows()


def go_to_add_to_database():
    global cam
    cam = cv2.VideoCapture(cam_port)
    start_camera(video_label, cam)

    database_window_btn.configure(text="Вернуться на главную", command=back_to_menu_from_database)
    add_to_database_btn.pack()
    name_label.pack()
    name_entry.pack()


def back_to_menu_from_face_recognition():
    face_recognition_window_btn.configure(text="Перейти к распознованию", command=go_to_face_recognition)
    cam.release()
    cv2.destroyAllWindows()


def go_to_face_recognition():
    global cam
    cam = cv2.VideoCapture(cam_port)
    face_recognition_window_btn.configure(text="Вернуться на главную", command=back_to_menu_from_face_recognition)
    show_face_recognition()


if __name__ == "__main__":
    window = tk.Tk()
    window.title("Main Menu")
    window.attributes("-topmost", True)
    window.geometry("1000x1000")

    database_window_btn = tk.Button(window, text="Добавить себя в базу", width=30, height=10,
                                    command=go_to_add_to_database)

    add_to_database_btn = tk.Button(window, text="Добавить в базу", width=20, height=5, command=adding_to_db)
    retake_photo_btn = tk.Button(window, text="Переснять", width=20, height=5, command=retake_camera_photo)

    name_label = tk.Label(window, text="Введите свое имя:")
    name_entry = tk.Entry(window)

    face_recognition_window_btn = tk.Button(window, text="Перейти к распознованию", width=30, height=10,
                                            command=go_to_face_recognition)

    video_label = tk.Label(window)
    database_window_btn.pack()
    face_recognition_window_btn.pack()

    window.mainloop()
