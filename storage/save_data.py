import json 
import os

def save_json(data, filepath):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open (filepath, "w", encoding= "utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent = 4)