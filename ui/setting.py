from .bg import set_background
from helpers.config import save_config
from tkinter import filedialog
import os

CONFIG_FILE = "config.json"
VOICE_OPTIONS = [
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-IN-NeerjaNeural",
    "en-GB-RyanNeural"
]


def open_settings(app, ctk, config, open_home):
    for widget in app.winfo_children():
        widget.destroy()

    set_background(app, ctk, config)

    shell = ctk.CTkFrame(
        app,
        fg_color="#08111f",
        corner_radius=34,
        border_width=1,
        border_color="#1f2a44"
    )
    shell.place(relx=0.5, rely=0.5, anchor="center",
                relwidth=0.88, relheight=0.82)

    form = ctk.CTkFrame(shell, fg_color="#0b1323", corner_radius=28)
    form.place(relx=0.06, rely=0.06, relwidth=0.88, relheight=0.88)

    ctk.CTkLabel(
        form,
        text="Customize",
        font=("Segoe UI Semibold", 30),
        text_color="#f8fafc"
    ).pack(pady=(30, 6))

    ctk.CTkLabel(
        form,
        text="Fine-tune your name, wake word, background, and voice.",
        font=("Segoe UI", 15),
        text_color="#cbd5e1"
    ).pack(pady=(0, 22))

    ctk.CTkLabel(form, text="Your name", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=36)
    user_entry = ctk.CTkEntry(form, width=500, placeholder_text="Your name")
    user_entry.insert(0, config.get("user_name", ""))
    user_entry.pack(padx=36, pady=(8, 18))

    ctk.CTkLabel(form, text="Wake name", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=36)
    wake_entry = ctk.CTkEntry(form, width=500, placeholder_text="Wake name")
    wake_entry.insert(0, config.get("wake_name", ""))
    wake_entry.pack(padx=36, pady=(8, 18))

    ctk.CTkLabel(form, text="Audio voice", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=36)
    voice_menu = ctk.CTkOptionMenu(form, values=VOICE_OPTIONS, width=500)
    voice_menu.set(config.get("voice", VOICE_OPTIONS[1]))
    voice_menu.pack(padx=36, pady=(8, 18))

    ctk.CTkLabel(form, text="Background", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=36)
    background_label = ctk.CTkLabel(
        form,
        text=os.path.basename(config.get("background", "assets/bg.png")),
        text_color="#93c5fd",
        font=("Segoe UI", 13)
    )
    background_label.pack(anchor="w", padx=36, pady=(8, 8))

    def choose_bg():
        file_path = filedialog.askopenfilename(
            filetypes=[("Images", "*.png *.jpg *.jpeg *.webp")]
        )
        if file_path:
            config["background"] = file_path
            background_label.configure(text=os.path.basename(file_path))

    ctk.CTkButton(
        form,
        text="Choose Background",
        command=choose_bg,
        fg_color="#0f172a",
        hover_color="#1e293b",
        border_width=1,
        border_color="#334155",
        corner_radius=18
    ).pack(padx=36, pady=(0, 18), anchor="w")

    status_label = ctk.CTkLabel(
        form, text="", text_color="#fda4af", font=("Segoe UI", 13))
    status_label.pack(pady=(4, 0))

    def save_settings():
        user_name = user_entry.get().strip()
        wake_name = wake_entry.get().strip()

        if not user_name or not wake_name:
            status_label.configure(
                text="Please keep both your name and the wake name filled in.")
            return

        config["user_name"] = user_name
        config["wake_name"] = wake_name
        config["voice"] = voice_menu.get()

        save_config(config_file=CONFIG_FILE, config=config)

        open_home(app, ctk, config, wake_name)

    ctk.CTkButton(
        form,
        text="Save Changes",
        command=save_settings,
        fg_color="#0f766e",
        hover_color="#115e59",
        corner_radius=18,
        height=42
    ).pack(padx=36, pady=(18, 12), fill="x")

    ctk.CTkButton(
        form,
        text="⬅ Back",
        command=lambda: open_home(app, ctk, config, config.get("wake_name")),
        fg_color="#111827",
        hover_color="#1f2937",
        border_width=1,
        border_color="#334155",
        corner_radius=18,
        height=40
    ).pack(padx=36, pady=(0, 18), fill="x")
