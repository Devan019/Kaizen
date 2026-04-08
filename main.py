from helpers.config import load_config
from ui import home, setup
import customtkinter as ctk
import speech_recognition as sr
from helpers.agent import Agent
from helpers.speak import speak_async
import threading

CONFIG_FILE = "config.json"

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("green")

#agent
agent = Agent()


# speech object and tool
r = sr.Recognizer()
# set thresold 1 sec
r.pause_threshold = 2

# speech fun

def start_listening(config):
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=2)

        while True:
            try:
                wake_name = (config.get("wake_name") or "").strip()
                voice = config.get("voice", "en-US-GuyNeural")

                print("Listening...")
                audio = r.listen(source)

                text: str = r.recognize_google(audio)
                print("You said:", text)

                if wake_name and wake_name.lower() in text.lower():
                    llm_res = agent.run_agent(text)
                    speak_async(llm_res, voice)

            except sr.UnknownValueError:
                print("Didn't catch that...")
                continue

            except sr.RequestError:
                print("API unavailable")
                continue

            except Exception as e:
                print("Error:", e)
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
