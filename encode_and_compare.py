import cv2
import dlib
import numpy as np


def compare_encodings(encoding, encodings_in_db):
    distance_threshold = 0.5
    distances = np.linalg.norm(np.array(encodings_in_db) - np.array(encoding), axis=1)
    matches = distances <= distance_threshold
    return np.any(matches)


def encode_faces(image, face_detector):
    shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
    face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_detector(gray)
    encodings = []

    for face in faces:
        landmarks = shape_predictor(gray, face)
        encoding = face_recognizer.compute_face_descriptor(image, landmarks)
        encodings.append(encoding)

    return encodings