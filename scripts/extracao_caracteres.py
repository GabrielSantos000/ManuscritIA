import os

TRANSCRIPTIONS_DIR = "ModeloML/dados/Treino/transcription"
OUTPUT_FILE = "ModeloML/dados/symbols.txt"

chars = set()

# Extrair caractéres das transcrição
for t in os.listdir(TRANSCRIPTIONS_DIR):
    if t.endswith(".txt"):
        with open(os.path.join(TRANSCRIPTIONS_DIR, t), "r", encoding="utf-8") as f:
            text = f.read()
            for c in text:
                chars.add(c)

# Ordenar (boa prática)
chars = sorted(chars)

with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    for c in chars:
        if c.strip() == "":
            f.write("<space>\n")  # padrão comum
        else:
            f.write(c + "\n")

print(f"Arquivo de símbolos gerado com {len(chars)} símbolos.")
