import cv2
import dlib
import numpy as np
import imutils

# Load face detector & landmark predictor
detector = dlib.get_frontal_face_detector()
predictor = dlib.shape_predictor("shape_predictor_68_face_landmarks.dat")

# Fungsi menggambar garis penanda
def draw_face_guides(frame, landmarks):
    left_eye = landmarks[42:48]
    right_eye = landmarks[36:42]
    nose = landmarks[27:36]
    mouth = landmarks[48:68]

    # Gambar & beri label
    if len(left_eye) == 6:
        cv2.polylines(frame, [left_eye], True, (0, 255, 0), 1)
        cv2.putText(frame, "Mata kiri", (left_eye[0][0], left_eye[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if len(right_eye) == 6:
        cv2.polylines(frame, [right_eye], True, (0, 255, 0), 1)
        cv2.putText(frame, "Mata kanan", (right_eye[0][0], right_eye[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)

    if len(nose) == 9:
        cv2.polylines(frame, [nose], True, (255, 0, 0), 1)
        cv2.putText(frame, "Hidung", (nose[0][0], nose[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 1)

    if len(mouth) == 20:
        cv2.polylines(frame, [mouth], True, (0, 0, 255), 1)
        cv2.putText(frame, "Mulut", (mouth[0][0], mouth[0][1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

# Fungsi cek apakah bagian terlihat (dengan toleransi)
def is_visible(part, min_area=5):
    return cv2.contourArea(part) > min_area

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
            cv2.putText(frame, "Tidak ada wajah terdeteksi", (10, 20),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

        for face in faces:
            landmarks = predictor(gray, face)
            points = np.array([(landmarks.part(n).x, landmarks.part(n).y) for n in range(68)], dtype=np.int32)

            left_eye = points[42:48]
            right_eye = points[36:42]
            nose = points[27:36]
            mouth = points[48:68]

            # Gambar panduan kalau bagian terlihat
            if is_visible(left_eye) or is_visible(right_eye) or is_visible(nose) or is_visible(mouth):
                draw_face_guides(frame, points)

            # Notifikasi bagian yang tidak terlihat
            if not is_visible(left_eye):
                cv2.putText(frame, "Mata kiri tidak terdeteksi", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            if not is_visible(right_eye):
                cv2.putText(frame, "Mata kanan tidak terdeteksi", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            if not is_visible(nose):
                cv2.putText(frame, "Hidung tidak terdeteksi", (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)
            if not is_visible(mouth):
                cv2.putText(frame, "Mulut tidak terdeteksi", (10, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255), 1)

        cv2.imshow("Face Landmark Guide", frame)

        if cv2.waitKey(1) & 0xFF == 27:  # ESC untuk keluar
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
