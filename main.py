from helpers.config import load_config
from ui import home, setup
import customtkinter as ctk
import speech_recognition as sr
from helpers.agent import Agent
from helpers.speak import speak_async
import threading
import time

CONFIG_FILE = "config.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

#agent
agent = Agent()


# speech object and tool
r = sr.Recognizer()

# speech fun

def start_listening(config):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=1)

        while True:
            try:
                wake_name = (config.get("wake_name") or "").strip()
                voice = config.get("voice", "en-US-GuyNeural")

                print("🎤 Listening...")

                # istening
                t_listen_start = time.perf_counter()
                audio = r.listen(source, timeout=2, phrase_time_limit=100)
                t_listen_end = time.perf_counter()

                #  STT
                t_stt_start = time.perf_counter()
                text: str = r.recognize_google(audio)
                t_stt_end = time.perf_counter()

                if wake_name and wake_name.lower() in text.lower():

                    # Agent
                    t_agent_start = time.perf_counter()
                    llm_res = agent.run_agent(text)
                    t_agent_end = time.perf_counter()

                    # TTS
                    t_tts_start = time.perf_counter()
                    speak_async(llm_res, voice)
                    t_tts_end = time.perf_counter()

                    print("\n⏱️ Timing Breakdown:")
                    print(f"Listening time: {t_listen_end - t_listen_start:.2f}s")
                    print(f"STT time: {t_stt_end - t_stt_start:.2f}s")
                    print(f"Agent time: {t_agent_end - t_agent_start:.2f}s")
                    print(f"TTS trigger time: {t_tts_end - t_tts_start:.2f}s")

            except Exception as e:
                print("❌ Error:", e)
                continue
# main
if __name__ == "__main__":
    app = ctk.CTk()
    app.title("Kaizen")
    app.after(0, lambda: app.state('zoomed'))

    config = load_config(CONFIG_FILE)

    if config["wake_name"] and config.get("user_name"):
        home.open_home(app, ctk, config, config["wake_name"])

        # listing thread
        listener_thread = threading.Thread(
            target=start_listening,
            args=(config,),
            daemon=True
        )

        listener_thread.start()

    else:
        setup.setup_ui(app, ctk, config, start_listening)

    app.mainloop()
