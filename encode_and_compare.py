import pickle
import numpy as np
import settings


def compare_encodings(encoding, encodings_in_db):
    distance_threshold = 0.5
    distances = np.linalg.norm(np.array(encodings_in_db) - np.array(encoding), axis=1)
    matches = distances <= distance_threshold
    return np.any(matches)


def encode_face(image, gray, face):
    landmarks = settings.shape_predictor(gray, face)
    encoding = settings.face_recognizer.compute_face_descriptor(image, landmarks)

    return encoding


