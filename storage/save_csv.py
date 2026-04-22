import csv
import os 

def save_csv(data, filepath):
    if not data:
        return 
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    fieldnames = data[0].keys()
    with open (filepath, "w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)