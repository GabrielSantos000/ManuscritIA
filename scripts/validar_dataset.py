import pandas as pd
from PIL import Image
import cv2

img = cv2.imread("ModeloML\img/14230.jpg")
print(img)

img = Image.open("ModeloML\img/14230.jpg")

# Carrega o CSV
df = pd.read_csv("ModeloML\datasetPaths.csv", encoding='latin1', sep= ";")

dataset = []
for _, row in df.iterrows():
    mat = row["matricula"]
    img_path = row["img_path"]
    txt_path = row["text_path"]

    with open(txt_path, "r", encoding="utf-8") as f:
        transcription = f.read().strip()

    dataset.append((img_path, transcription))

#print(dataset)

# Percorre cada linha
for i, t in dataset:
    img_path = i
    transcription = t

    # Carrega a imagem
    img = Image.open(img_path)

    print(f"Imagem: {img}\n\n")
    print(f"Transcrição correta: {transcription}")
    print("-" * 40)