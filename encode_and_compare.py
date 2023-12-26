import pickle
import numpy as np
import settings
from dataBaseConnect import connection


def compare_encodings(encoding, encodings_in_db):
    distance_threshold = 0.5
    distances = np.linalg.norm(np.array(encodings_in_db) - np.array(encoding), axis=1)
    matches = distances <= distance_threshold
    return np.any(matches)


def encode_face(image, gray, faces):
    if not faces:
        return []

    landmarks = settings.shape_predictor(gray, faces[0])
    encoding = settings.face_recognizer.compute_face_descriptor(image, landmarks)

    encodings = []

    for face in faces:
        landmarks = settings.shape_predictor(gray, face)
        encoding = settings.face_recognizer.compute_face_descriptor(image, landmarks)
        encodings.append(encoding)

    return encodings


def check_duplicate_encodings(encoding):
    cursor = connection.cursor()
    cursor.execute("SELECT encodings FROM face_encodings")
    encodings_in_db = cursor.fetchall()

    for encodings in encodings_in_db:
        encodings = pickle.loads(encodings[0])
        if compare_encodings(encoding, encodings):
            return True

    return False
