import pickle
import numpy as np
import settings
from dataBaseConnect import connection


def compare_encodings(encodings, encodings_in_db):
    distances = np.linalg.norm(np.array(encodings_in_db) - np.array(encodings), axis=1)

    if distances <= settings.distance_threshold:
        return True

    return False


def encode_face(image, gray, faces):
    if not faces:
        return []

    encodings = []

    for face in faces:
        landmarks = settings.shape_predictor(gray, face)
        encoding = settings.face_recognizer.compute_face_descriptor(image, landmarks)
        encodings.append(encoding)

    return encodings


def check_duplicate_encodings(encoding):
    cursor = connection.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS face_encodings (id SERIAL PRIMARY KEY, name VARCHAR(255), encodings BYTEA)"
    )
    cursor.execute("SELECT encodings FROM face_encodings")
    encodings_in_db = cursor.fetchall()

    for encodings in encodings_in_db:
        encodings = pickle.loads(encodings[0])
        if compare_encodings(encoding, encodings):
            return True

    return False
