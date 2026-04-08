import os
import json


CONFIG_FILE = "config.json"


def load_config(config_file):
    default = {
        "user_name": "",
        "wake_name": None,
        "voice": "en-US-GuyNeural",
        "background": "assets/bg.png"
    }

    if os.path.exists(config_file):
        with open(config_file) as f:
            json_data = json.load(f)
            default.update(json_data)

    return default


def save_config(config_file, config):
    with open(config_file, "w") as f:
        json.dump(config, f, indent=4)


def save_wake_name(app, ctk, config, status_label, entry, open_home, config_file=CONFIG_FILE):
    wake_name = entry.get().strip()

    if not wake_name:
        status_label.configure(text="Enter a wake name ❌")
        return

    config["wake_name"] = wake_name
    save_config(config_file, config)

    open_home(app, ctk, config, wake_name)
