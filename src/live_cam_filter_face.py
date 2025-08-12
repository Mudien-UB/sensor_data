import cv2
import dlib
import numpy as np
import imutils

# Load face detector & landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

def draw_eye_bar(frame, left_eye_points, right_eye_points):
    all_eye_points = np.concatenate((left_eye_points, right_eye_points))
    x, y, w, h = cv2.boundingRect(all_eye_points)
    pad_y = int(h * 0.5)
    pad_x = int(w * 0.5)
    cv2.rectangle(
        frame,
        (x - pad_x, y - pad_y),
        (x + w + pad_x, y + h + pad_y),
        (0, 0, 0),
        -1
    )

def draw_mouth_x(frame, mouth_points):
    x, y, w, h = cv2.boundingRect(mouth_points)
    cv2.line(frame, (x, y), (x + w, y + h), (0, 0, 255), 2)
    cv2.line(frame, (x + w, y), (x, y + h), (0, 0, 255), 2)

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)

        if len(faces) == 0:
            # Buat blur hitam-putih
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray_frame, (51, 51), 0)
            frame = cv2.cvtColor(blurred, cv2.COLOR_GRAY2BGR)

        else:
            for face in faces:
                landmarks = predictor(gray, face)
                points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)], dtype=np.int32)

                left_eye = points[42:48]
                right_eye = points[36:42]
                mouth = points[48:68]

                draw_eye_bar(frame, left_eye, right_eye)
                draw_mouth_x(frame, mouth)

        cv2.imshow("Face Sensor", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
