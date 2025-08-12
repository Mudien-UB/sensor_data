import cv2
import dlib
import numpy as np
import imutils

# Detector wajah dari dlib
detector = dlib.get_frontal_face_detector()

# Fungsi menggambar kotak transparan di wajah
def draw_box(frame, face):
    # Ambil koordinat bounding box wajah
    x1 = face.left()
    y1 = face.top()
    x2 = face.right()
    y2 = face.bottom()

    # Overlay transparan
    overlay = frame.copy()
    alpha = 0.5  # transparansi

    cv2.rectangle(overlay, (x1, y1), (x2, y2), (0, 0, 0), -1)  # kotak hitam
    cv2.addWeighted(overlay, alpha, frame, 1 - alpha, 0, frame)

def main():
    cap = cv2.VideoCapture(0)

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        faces = detector(gray)
        for face in faces:
            draw_box(frame, face)

        cv2.imshow("Live camera filter box, Mudien", frame)

        key = cv2.waitKey(1) & 0xFF
        if key == 27:  # tekan ESC untuk keluar
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
