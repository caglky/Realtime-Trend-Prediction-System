import json
import os

def load_json(filepath):
    if not os.path.exists(filepath):
        return None
    with open(filepath, "r", encoding="utf-8") as file:
        return json.load(file)