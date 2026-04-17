from .setting import open_settings
from .bg import set_background
from helpers.speak import speak_async
from datetime import datetime
import random
import threading


def open_home(app, ctk, config, wake_name=None):
    for widget in app.winfo_children():
        widget.destroy()

    # This will load your robotic arm background image
    set_background(app, ctk, config)

    wake_name = (wake_name or config.get("wake_name") or "Jarvis").strip()
    user_name = (config.get("user_name") or "").strip() or "Pilot"
    location = (config.get("weather_city") or config.get(
        "location") or "Vadodara, GJ").strip()

    lines = [
        f"SYSTEM ONLINE. WELCOME BACK, {user_name.upper()}.",
        f"CORE INITIALIZED. {wake_name.upper()} AT YOUR SERVICE.",
        f"ALL SYSTEMS NOMINAL. READY FOR INPUT, {user_name.upper()}.",
    ]

    text = random.choice(lines)

    threading.Thread(
        target=speak_async,
        args=(text, config["voice"]),
        daemon=True
    ).start()

    # --- TOP LEFT: STATUS & LOCATION ---
    ctk.CTkLabel(
        app,
        text="STATUS: NOMINAL",
        font=("Consolas", 22),
        text_color="#dbeafe",
        fg_color="transparent",
        bg_color="transparent" 
    ).place(relx=0.08, rely=0.08, anchor="nw")

    ctk.CTkLabel(
        app,
        text=f"LOCATION: {location.upper()}",
        font=("Consolas", 20),
        text_color="#00f2ff",  # Neon Cyan
        fg_color="transparent",
         bg_color="transparent" 
    ).place(relx=0.08, rely=0.13, anchor="nw")

    # --- TOP RIGHT: SYSTEM TELEMETRY (CLOCK) ---
    clock_label = ctk.CTkLabel(
        app,
        text="--:--:--",
        font=("Consolas", 72, "bold"),
        text_color="#00f2ff",  # Neon Cyan
        fg_color="transparent",
         bg_color="transparent" 
    )
    clock_label.place(relx=0.92, rely=0.10, anchor="ne")

    date_label = ctk.CTkLabel(
        app,
        text="-- --- ----",
        font=("Consolas", 18),
        text_color="#dbeafe",
        fg_color="transparent",
         bg_color="transparent" 
    )
    date_label.place(relx=0.92, rely=0.19, anchor="ne")

    # --- BOTTOM CENTER: COMMAND CORE & INTRO ---
    dynamic_label = ctk.CTkLabel(
        app,
        text="CENTRALIZED COMMAND UNIT - OPTIMAL PERFORMANCE",
        font=("Consolas", 16),
        text_color="#00f2ff",
        fg_color="transparent",
         bg_color="transparent" 
    )
    dynamic_label.place(relx=0.5, rely=0.80, anchor="center")

    ctk.CTkLabel(
        app,
        text=f"⟦ {wake_name.upper()} ⟧",
        font=("Consolas", 52, "bold"),
        text_color="#ffffff",
        fg_color="transparent",
         bg_color="transparent" 
    ).place(relx=0.5, rely=0.87, anchor="center")

    footer_text = (
        "COMMAND INTERFACE & COGNITIVE ASSISTANT | EST. 2023 | PERSONALIZED AI ARCHITECTURE\n"
        "CORE FUNCTIONS INCLUDE: COMPLEX PROBLEM SOLVING, AUTOMATION, DATA ANALYSIS, AND CONTEXTUAL RESPONSES."
    )
    footer_label = ctk.CTkLabel(
        app,
        text=footer_text,
        font=("Consolas", 10),
        text_color="#93c5fd",
        fg_color="transparent",
        justify="center",
         bg_color="transparent" 
    )
    footer_label.place(relx=0.5, rely=0.94, anchor="center")

   

    def update_overlay_time():
        now = datetime.now()
        try:
            clock_label.configure(text=now.strftime("%H:%M:%S"))
            date_label.configure(text=now.strftime("%d %b %Y").upper())
            app.after(1000, update_overlay_time)
        except Exception:
            return


    update_overlay_time()