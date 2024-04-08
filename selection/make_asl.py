import json
import os
import shutil
import csv

if not os.path.exists("asl"):
    os.makedirs("asl")

with open("selected.json") as f:
    selected = json.load(f)
    
csv_data = []
for gloss in selected:
    shutil.copy2(f"poses/{selected[gloss]}.pose", f"asl/{gloss}.pose")
    csv_data.append({
        "path": f"asl/{gloss}.pose",
        "spoken_language": "en",
        "signed_language": "asl",
        "start": 0,
        "end": 0,
        "words": gloss,
        "glosses": gloss,
        "priority": 0
    })
    
csv_filename = "index.csv"
with open(csv_filename, mode="w", newline="") as file:
    fieldnames = ["path", "spoken_language", "signed_language", "start", "end", "words", "glosses", "priority"]
    writer = csv.DictWriter(file, fieldnames=fieldnames)
    
    writer.writeheader()
    for row in csv_data:
        writer.writerow(row)
