from .setting import open_settings
from .bg import set_background
from helpers.speak import speak_async
import random
import threading


def open_home(app, ctk, config, wake_name=None):
    for widget in app.winfo_children():
        widget.destroy()

    set_background(app, ctk, config)

    wake_name = (wake_name or config.get("wake_name") or "Kaizen").strip()
    user_name = (config.get("user_name") or "").strip() or "there"

    lines = [
        f"Good to see you, {user_name}. I’m {wake_name}. What would you like to do next?",
        f"{wake_name} is ready, {user_name}. Give me a task whenever you are ready.",
        f"Hello {user_name}, I’m {wake_name}. I’m listening.",
    ]

    text = random.choice(lines)

    threading.Thread(
        target=speak_async,
        args=(text, config["voice"]),
        daemon=True
    ).start()

    # Settings Button
    settings_btn = ctk.CTkButton(
        app,
        text="⚙ Customize",
        command=lambda: open_settings(app, ctk, config, open_home),
        fg_color="#0f172a",
        hover_color="#1e293b",
        border_width=1,
        border_color="#334155",
        corner_radius=18
    )
    settings_btn.place(relx=0.95, rely=0.05, anchor="ne")
