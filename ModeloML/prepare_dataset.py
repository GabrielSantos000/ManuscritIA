import pandas as pd
import os
import shutil
from sklearn.model_selection import train_test_split

CSV_PATH = "ModeloML/dfnovo.csv"
OUT_DIR = "ModeloML/dados"

df = pd.read_csv(CSV_PATH, sep=";", encoding="utf-8")

# Separar parte do df para treino de forma aleatória
train_df, val_df = train_test_split(df, test_size=0.1, random_state=42)

def process_split(split_df, split_name):
    img_dir = os.path.join(OUT_DIR, split_name, "images")
    txt_dir = os.path.join(OUT_DIR, split_name, "texts")

    # Abrir novas pastas, caso não exista
    os.makedirs(img_dir, exist_ok=True)
    os.makedirs(txt_dir, exist_ok=True)

    for idx, row in split_df.iterrows():
        img_name = f"{row['matricula']}.png"
        txt_name = f"{row['matricula']}.txt"

        shutil.copy(row["img_path"], os.path.join(img_dir, img_name))

        with open(os.path.join(txt_dir, txt_name), "w", encoding="utf-8") as f:
            f.write(open(row["texto_corrigido"], encoding="utf-8").read())


process_split(train_df, "train")
process_split(val_df, "val")

print("Dataset preparado com sucesso.")
