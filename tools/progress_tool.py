import json
import os

FILE_PATH = "data/progress.json"


def load_progress():
    if not os.path.exists(FILE_PATH):
        return {}

    with open(FILE_PATH, "r") as f:
        return json.load(f)


def save_progress(progress):
    with open(FILE_PATH, "w") as f:
        json.dump(progress, f, indent=4)