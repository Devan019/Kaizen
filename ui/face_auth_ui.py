import customtkinter as ctk
import cv2
from PIL import Image, ImageTk
from deepface import DeepFace
import os

FACE_IMAGE = "face.jpg"


class FaceAuthUI(ctk.CTkFrame):
    def __init__(self, parent, on_success):
        super().__init__(parent, fg_color="transparent")
        self.loading = False

        self.on_success = on_success
        self.cap = cv2.VideoCapture(0)

        self.label = ctk.CTkLabel(
            self, text="🔐 Face Unlock", font=("Arial", 24))
        self.label.pack(pady=20)

        self.instruction = ctk.CTkLabel(
            self, text="Look at the camera...", font=("Arial", 16)
        )
        self.instruction.pack(pady=10)

        self.video_label = ctk.CTkLabel(self, text="")
        self.video_label.pack()

        self.status = ctk.CTkLabel(self, text="", text_color="red")
        self.status.pack(pady=10)

        self.after(10, self.update_frame)

    def run_loader(self):
        if self.loader_cycles >= 6:  # ~2 sec (6 * 300ms)
            self.status.configure(text="🚀 Welcome!", text_color="green")
            self.after(500, self.on_success)
            return

        text = self.loader_states[self.loader_index]
        self.status.configure(text=text)

        self.loader_index = (self.loader_index + 1) % len(self.loader_states)
        self.loader_cycles += 1

        self.after(300, self.run_loader)

    def animate_loader(self):
        self.loader_states = ["🔓 Unlocking.",
                              "🔓 Unlocking..", "🔓 Unlocking..."]
        self.loader_index = 0
        self.loader_cycles = 0

        self.run_loader()

    def update_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            self.after(10, self.update_frame)
            return

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(rgb)
        imgtk = ImageTk.PhotoImage(image=img)

        self.video_label.imgtk = imgtk
        self.video_label.configure(image=imgtk)

        # 🔐 Face verify
        try:
            result = DeepFace.verify(
                img1_path=FACE_IMAGE,
                img2_path=frame,
                enforce_detection=False
            )

            if result["verified"]:
                self.status.configure(
                    text="✅ Access Granted", text_color="green")
                self.cap.release()
                self.animate_loader()
                return
            else:
                self.status.configure(text="❌ Not matched")

        except Exception:
            pass

        self.after(200, self.update_frame)
