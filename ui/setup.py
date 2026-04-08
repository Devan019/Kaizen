from .bg import set_background
from helpers.config import save_config
from .home import open_home
from tkinter import filedialog
import os

CONFIG_FILE = "config.json"
VOICE_OPTIONS = [
    "en-US-JennyNeural",
    "en-US-GuyNeural",
    "en-IN-NeerjaNeural",
    "en-GB-RyanNeural"
]


def setup_ui(app, ctk, config, start_listening=None):
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

    hero = ctk.CTkFrame(shell, fg_color="#0e1728", corner_radius=28)
    hero.place(relx=0.03, rely=0.05, relwidth=0.36, relheight=0.9)

    form = ctk.CTkFrame(shell, fg_color="#0b1323", corner_radius=28)
    form.place(relx=0.42, rely=0.05, relwidth=0.55, relheight=0.9)

    ctk.CTkLabel(
        hero,
        text="Kaizen",
        font=("Segoe UI Semibold", 42),
        text_color="#f8fafc"
    ).pack(pady=(52, 12), padx=32, anchor="w")

    ctk.CTkLabel(
        hero,
        text="Let's personalize your assistant before it starts listening.",
        font=("Segoe UI", 17),
        text_color="#cbd5e1",
        wraplength=340,
        justify="left"
    ).pack(pady=(0, 18), padx=32, anchor="w")

    ctk.CTkLabel(
        hero,
        text="You only need to set this up once.",
        font=("Segoe UI", 14),
        text_color="#94a3b8"
    ).pack(pady=(0, 20), padx=32, anchor="w")

    ctk.CTkLabel(
        hero,
        text="What you can choose",
        font=("Segoe UI Semibold", 14),
        text_color="#7dd3fc"
    ).pack(pady=(16, 10), padx=32, anchor="w")

    for item in [
        "Your name",
        "Wake name",
        "Audio voice",
        "Background image"
    ]:
        ctk.CTkLabel(
            hero,
            text=f"• {item}",
            font=("Segoe UI", 15),
            text_color="#dbeafe"
        ).pack(pady=3, padx=38, anchor="w")

    ctk.CTkLabel(
        form,
        text="Welcome Setup",
        font=("Segoe UI Semibold", 28),
        text_color="#f8fafc"
    ).pack(pady=(34, 6))

    ctk.CTkLabel(
        form,
        text="Tell me who you are, what I should answer to, and how I should sound.",
        font=("Segoe UI", 15),
        text_color="#cbd5e1",
        wraplength=520,
        justify="center"
    ).pack(padx=34, pady=(0, 24))

    ctk.CTkLabel(form, text="Your name", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=34)
    user_entry = ctk.CTkEntry(
        form, width=420, placeholder_text="What should I call you?")
    user_entry.insert(0, config.get("user_name", ""))
    user_entry.pack(padx=34, pady=(8, 18))

    ctk.CTkLabel(form, text="Wake name", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=34)
    wake_entry = ctk.CTkEntry(
        form, width=420, placeholder_text="Say my name to wake me up")
    wake_entry.insert(0, config.get("wake_name", ""))
    wake_entry.pack(padx=34, pady=(8, 18))

    ctk.CTkLabel(form, text="Audio voice", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=34)
    voice_menu = ctk.CTkOptionMenu(form, values=VOICE_OPTIONS, width=420)
    voice_menu.set(config.get("voice", VOICE_OPTIONS[1]))
    voice_menu.pack(padx=34, pady=(8, 18))

    ctk.CTkLabel(form, text="Background", font=(
        "Segoe UI Semibold", 14)).pack(anchor="w", padx=34)
    background_label = ctk.CTkLabel(
        form,
        text=os.path.basename(config.get("background", "assets/bg.png")),
        text_color="#93c5fd",
        font=("Segoe UI", 13)
    )
    background_label.pack(anchor="w", padx=34, pady=(8, 8))

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
    ).pack(padx=34, pady=(0, 18), anchor="w")

    status_label = ctk.CTkLabel(
        form, text="", text_color="#fda4af", font=("Segoe UI", 13))
    status_label.pack(pady=(4, 0))

    def save_setup():
        user_name = user_entry.get().strip()
        wake_name = wake_entry.get().strip()

        if not user_name or not wake_name:
            status_label.configure(
                text="Please add both your name and a wake name.")
            return

        config["user_name"] = user_name
        config["wake_name"] = wake_name
        config["voice"] = voice_menu.get()

        save_config(CONFIG_FILE, config)
        open_home(app, ctk, config, wake_name)

        if callable(start_listening):
            import threading

            threading.Thread(
                target=start_listening,
                args=(config,),
                daemon=True
            ).start()

    ctk.CTkButton(
        form,
        text="Start Kaizen",
        command=save_setup,
        fg_color="#0f766e",
        hover_color="#115e59",
        corner_radius=18,
        height=42
    ).pack(padx=34, pady=(18, 12), fill="x")
