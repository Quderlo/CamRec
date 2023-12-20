import pickle
from tkinter import messagebox

import cv2
import dlib
from PIL import Image, ImageTk

from dataBaseConnect import connection
from encode_and_compare import encode_faces, compare_encodings


def check_duplicate_encodings(encoding):
    cursor = connection.cursor()
    cursor.execute("SELECT encodings FROM face_encodings")
    encodings_in_db = cursor.fetchall()

    for encodings in encodings_in_db:
        encodings = pickle.loads(encodings[0])
        if compare_encodings(encoding, encodings):
            return True

    return False


def add_to_db(cam, name_entry):
    face_detector = dlib.get_frontal_face_detector()

    name = name_entry.get()

    if name != "":
        ret, image = cam.read()

        if ret:
            encodings = encode_faces(image, face_detector)

            if len(encodings) > 0:
                byte_data = pickle.dumps(encodings)
                print("Кодировки лиц в байтах:", byte_data)
                print("Лицо найдено")

                if not check_duplicate_encodings(encodings):
                    cursor = connection.cursor()
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS face_encodings (id SERIAL PRIMARY KEY, name VARCHAR(255), encodings BYTEA)"
                    )
                    cursor.execute(
                        "INSERT INTO face_encodings (name, encodings) VALUES (%s, %s)",
                        (name, byte_data)
                    )
                    connection.commit()
                else:
                    messagebox.showinfo("Ошибка", "Похожий на вас пользователь уже зарегистрирован")
            else:
                print("Лицо не найдено")
        else:
            print("Не удалось считать кадр с камеры")
    else:
        messagebox.showinfo("Ошибка", "Пожалуйста, введите имя")


def start_camera(video_label, cam):
    # Инициализация детектора лиц
    face_detector = dlib.get_frontal_face_detector()

    # Создание таблицы, если она не существует
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS face_encodings (id SERIAL PRIMARY KEY, name VARCHAR(255), encodings BYTEA)"
    )

    def show_frame():

        # Запуск отображения кадра
        ret, frame = cam.read()  # Получение кадра с камеры

        if not ret:
            # Если кадр пустой, останавливаем отображение
            return

        # Преобразование кадра в оттенки серого
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Выполнение детектирования лиц в кадре
        faces = face_detector(gray)


        # Рисуем прямоугольник вокруг каждого найденного лица
        for face in faces:
            x, y, w, h = face.left(), face.top(), face.width(), face.height()
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Преобразование кадра в изображение Pillow
        img = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
        imgtk = ImageTk.PhotoImage(image=img)

        # Обновление изображения в окне Tkinter
        video_label.imgtk = imgtk
        video_label.configure(image=imgtk)

        # Запуск отображения нового кадра через определенный интервал времени
        video_label.after(10, show_frame)

    # Создание метки для отображения изображения
    video_label.pack()
    show_frame()
