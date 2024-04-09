import json
import os
import shutil

if not os.path.exists("asl"):
    os.makedirs("asl")

with open("selected.json") as f:
    selected = json.load(f)
    
words = []
for gloss in selected:
    shutil.copy2(f"poses/{selected[gloss]}.pose", f"asl/{gloss}.pose")
    words.append(gloss.lower().strip())
    
words_file = "words.txt"
with open(words_file, mode="w") as file:
    file.write("\n".join(words))
