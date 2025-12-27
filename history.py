import json
import os

FILE = "chat_history.json"

def init():
    if not os.path.exists(FILE) or os.path.getsize(FILE) == 0:
        with open(FILE, "w") as f:
            json.dump({}, f)

init()

def save_history(user, entry):
    init()
    with open(FILE, "r") as f:
        data = json.load(f)

    data.setdefault(user, []).append(entry)

    with open(FILE, "w") as f:
        json.dump(data, f, indent=4)

def load_history(user):
    init()
    with open(FILE, "r") as f:
        return json.load(f).get(user, [])
