import cv2
import dlib
import pickle
from dataBaseConnect import connection


def addToDataBase():
    cam_port = 0
    cam = cv2.VideoCapture(cam_port)

    # Инициализация детектора лиц
    face_detector = dlib.get_frontal_face_detector()
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

    # Создайте курсор
    cursor = connection.cursor()

    # Создайте таблицу, если она не существует
    cursor.execute("CREATE TABLE IF NOT EXISTS face_encodings (id SERIAL PRIMARY KEY, name VARCHAR(255), encodings BYTEA)")

    # Считываем один кадр с камеры
    result, image = cam.read()

    if result:
        # Преобразование изображения в оттенки серого
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Выполнение детектирования лиц в кадре
        faces = face_detector(gray)

        if len(faces) > 0:
            # Кодирование лица
            encodings = []
            for face in faces:
                landmarks = shape_predictor(gray, face)
                encoding = face_recognizer.compute_face_descriptor(image, landmarks)
                encodings.append(encoding)
            print("Кодировки лиц:", encodings)
            byte_data = pickle.dumps(encodings)
            print("Кодировки лиц в байтах:", byte_data)
            print("Лицо найдено")

            # Введите имя пользователя
            name = input("Введите ваше имя: ")

            # Добавьте имя пользователя и байтовые данные в базу данных
            cursor.execute("INSERT INTO face_encodings (name, encodings) VALUES (%s, %s)", (name, byte_data))
            connection.commit()
        else:
            print("Лицо не найдено")

        # сохраняем фото в файл
        cv2.imwrite("photo.jpg", image)

    else:
        print("No image detected. Please try again")

    # Закройте курсор и соединение с базой данных
    cursor.close()
    connection.close()

    # освобождаем ресурсы
    cam.release()
