import dlib

frame_count = 30
skipping_frames = False
cam_port = 0
window_size = "1000x1000"

face_detector = dlib.get_frontal_face_detector()
shape_predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("dlib_face_recognition_resnet_model_v1.dat")

face_rectangle_color = (0, 255, 0)
