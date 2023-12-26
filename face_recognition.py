import cv2
import pickle
from dataBaseConnect import connection
from encode_and_compare import compare_encodings
import settings


def show_face_recognition():
    cam = cv2.VideoCapture(settings.cam_port)

    count = 0

    cursor = connection.cursor()

    while True:
        result, image = cam.read()

        if result:
            gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

            faces = settings.face_detector(gray)

            encodings = []

            cursor.execute("SELECT name, encodings FROM face_encodings")
            rows = cursor.fetchall()

            for face in faces:
                x, y, w, h = face.left(), face.top(), face.width(), face.height()
                cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0, 0), 2)

                if (not settings.skipping_frames) or (settings.skipping_frames and count % settings.frame_count == 0):
                    landmarks = settings.shape_predictor(gray, face)
                    encoding = settings.face_recognizer.compute_face_descriptor(image, landmarks)
                    encodings.append(encoding)

                    found_match = False
                    name = None
                    for row in rows:
                        db_encodings = pickle.loads(row[1])
                        if compare_encodings(encodings[0], db_encodings):
                            name = row[0]
                            found_match = True
                            break

                    if found_match and name:
                        cv2.putText(image, name, (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)
                    elif len(encodings) >= 0:
                        cv2.putText(image, "Neznakomec", (x, y + h + 30), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 0, 255), 2)

            count += 1

            cv2.imshow("Face Recognition", image)

            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                cam.release()
                cv2.destroyAllWindows()
                cursor.close()
                connection.close()
                break

        else:
            print("No image detected. Please try again")
