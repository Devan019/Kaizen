import cv2
import os
import time
from deepface import DeepFace

FACE_IMAGE = "face.jpg"


# 📸 Register face
def register_face():
    cap = cv2.VideoCapture(0)

    print("📸 Capturing face... Look at camera")

    count = 0
    best_frame = None

    while count < 20:  # capture multiple frames
        ret, frame = cap.read()
        if not ret:
            continue

        best_frame = frame  # keep updating (latest frame)
        count += 1

        cv2.imshow("Register Face", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

        time.sleep(0.1)

    cap.release()
    cv2.destroyAllWindows()

    if best_frame is not None:
        cv2.imwrite(FACE_IMAGE, best_frame)
        print("✅ Face registered!")
    else:
        print("❌ Failed to capture face")


# 🔐 Authenticate
def authenticate_face():
    if not os.path.exists(FACE_IMAGE):
        print("⚠️ No face registered. Registering now...")
        register_face()

    cap = cv2.VideoCapture(0)

    print("🔐 Authenticating...")

    while True:
        ret, frame = cap.read()
        if not ret:
            continue

        temp_img = "temp.jpg"
        cv2.imwrite(temp_img, frame)

        try:
            result = DeepFace.verify(
                img1_path=FACE_IMAGE,
                img2_path=temp_img,
                enforce_detection=False  # avoid crash if face not found
            )

            if result["verified"]:
                print("✅ Access Granted")
                cap.release()
                cv2.destroyAllWindows()
                os.remove(temp_img)
                return True

        except Exception as e:
            print("Error:", e)

        cv2.imshow("Face Unlock", frame)

        if cv2.waitKey(1) & 0xFF == 27:
            break

    cap.release()
    cv2.destroyAllWindows()
    return False