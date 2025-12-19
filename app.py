# Interface
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap.constants import *
import customtkinter

# Reconhecimento e transcrição de textos manuscritos
from kraken import binarization, pageseg, rpred
from kraken.lib import models

# Importação e leitura de imagens
from PIL import Image, ImageTk

# Leitura e processamentos do dataframe
import pandas as pd

# Acesso ao sistema do computador
import os
import subprocess

# Caminho do dataframe
dfCSV = "ModeloML\dfnovo.csv"

# Criar um dataframe CSV se não existir
if not os.path.exists(dfCSV):
    pd.DataFrame(
        columns=["matricula", "img_path", "texto_corrigido", "ocr_text"]
    ).to_csv(dfCSV, index=False, sep=";", encoding="utf-8")


# Função para processar imagem com Kraken OCR
def process_imagem(img_path, model_path="modelo_matriculas.mlmodel"):
    imagem = Image.open(img_path)  # Abre a imagem

    f = 3  # Factor de redimensionamento
    im = imagem.resize(
        (imagem.width * f, imagem.height * f), Image.LANCZOS
    )  # Redimensiona a imagem aumentando em 3x

    # Renomeação do caminho da imagem e da extensão
    pasta_saida = "ModeloML/img_processadas"
    os.makedirs(pasta_saida, exist_ok=True)  # Cria uma pasta se não existir ainda
    nome_base = os.path.splitext(os.path.basename(img_path))[0]  # Separa o nome da extensão (nome.png --> (nome, .png))
    new_path = os.path.join(pasta_saida, f"{nome_base}.png")  # novo caminho da imagem

    im.save(new_path, dpi=(300, 300))  # Salva com metadado de 300 dpi
    img_cinza = im.convert("L")  # Coloca imagem em tons de cinza

    im_bin = binarization.nlbin(img_cinza)  # Binariza a imagem
    seg_linha = pageseg.segment(im_bin)  # Faz a segmentação de linhas
    ocr_model = rpred.load_any(model_path)  # Carrega o modelo OCR
    pred = rpred.rpred(ocr_model, im_bin, seg_linha)  # Faz a predição

    texto = "\n".join([line.prediction for line in pred])
    return texto


# Função para salvar a correção no dataframe
def save_correcao(matricula, img_path, txt_ocr_path, txt_corrigido_path):
    df = pd.read_csv(dfCSV, sep=";", encoding="utf-8")
    df = pd.concat(
        [
            df,
            pd.DataFrame(
                [
                    {
                        "matricula": matricula,
                        "img_path": img_path,
                        "texto_corrigido": txt_corrigido_path,
                        "ocr_text": txt_ocr_path,
                    }
                ]
            ),
        ],
        ignore_index=True,
    )
    df.to_csv(dfCSV, sep=";", encoding="utf-8", index=False)  # Atualizar dataframe
    messagebox.showinfo("Feedback", "Correção salva no dataframe!")

    import pandas as pd


def treinar():
    subprocess.Popen(["bash", "ModeloML\script-treino.sh"])


# Interface
def app_manuscritIA():
    root = customtkinter.CTk()
    customtkinter.set_default_color_theme("dark-blue")
    root.title("ManuscritIA - Transcrição OCR de Manuscritos")
    root.iconbitmap("logo_sistema.ico")
    root.geometry("1200x600")  # Largura x Altura em pixels

    # Definição do grid da janela principal
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)
    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=2)

    # ---------------- DESIGN E ORGANIZAÇÃO LAYOUT ------------------------------

    # Área da imagem------------------------
    img_label = customtkinter.CTkLabel(
        root,
        text="Imagem da Matrícula",
        font=("Arial", 12, "bold"),
        height=40,
        bg_color="#141414",
        corner_radius=20,
    )
    img_label.grid(row=0, column=0, sticky="nsew", padx=2, pady=2)

    img_box = customtkinter.CTkLabel(root, text="")
    img_box.grid(row=1, column=0, sticky="nsew")

    # Área do texto-------------------------
    text_label = customtkinter.CTkLabel(
        root,
        text="Texto Extraído",
        font=("Arial", 12, "bold"),
        height=40,
        bg_color="#141414",
        corner_radius=20,
    )
    text_label.grid(row=0, column=1, sticky="nsew", padx=2, pady=2)

    text_box = customtkinter.CTkTextbox(root, width=15, height=40, font=("Arial", 12))
    scroll2 = tk.Scrollbar(root, command=text_box.yview)
    text_box.configure(yscrollcommand=scroll2.set)
    text_box.grid(column=1, row=1, sticky="nsew")

    # Label Matrícula
    # mat_label = customtkinter.CTkLabel(root, text="Matrícula", font=("Arial", 12, "bold"))
    # mat_label.grid(row=2, column=1, sticky="nsew")

    # Campo Matrícula
    entry_matricula = customtkinter.CTkEntry(
        root,
        font=("Arial", 12),
        justify="center",
        placeholder_text="Digite a matrícula aqui",
        height=15,
    )
    entry_matricula.grid(
        row=2, column=1, sticky="nsew", ipadx=5, ipady=5, padx=2, pady=2
    )

    img_path_var = tk.StringVar()
    ocr_text_var = tk.StringVar()

    # Upload da imagem
    def upload_image():
        file_path = filedialog.askopenfilename(
            filetypes=[("Imagens", "*.jpg *.png *.jpeg")]
        )
        matricula = entry_matricula.get()
        if not matricula.strip():
            messagebox.showwarning("Aviso", "Por favor, digite a matrícula!")
            return

        if file_path:
            try:
                texto = process_imagem(
                    file_path
                )  # Transcreve o texto da imagem e armazena na variável texto
                text_box.delete("1.0", tk.END)  # Apaga todo conteúdo da caixa de texto
                text_box.insert(tk.END, texto)  # Adiciona o texto gerado pela OCR
                img_path_var.set(file_path)  # Guarda o caminho da imagem selecionada
                ocr_text_var.set(texto)  # Guarda o texto lido pela IA

                # Exibe imagem com redimensionamento
                im = Image.open(file_path)
                im.thumbnail((1195, 1600))  # tamanho inicial
                tk_img = ImageTk.PhotoImage(im)
                img_box.config(image=tk_img)
                img_box.image = tk_img

                messagebox.showinfo("Sucesso", "Upload realizado com sucesso!")

            except Exception as e:
                messagebox.showerror("Erro", f"Falha no OCR: {e}")

    # Zoom na imagem
    def zoom_image(factor=1.5):
        file_path = img_path_var.get()
        if file_path:
            im = Image.open(file_path)
            largura, altura = im.size
            im = im.resize((int(largura * factor), int(altura * factor)))
            tk_img = ImageTk.PhotoImage(im)
            img_label.config(image=tk_img)
            img_label.image = tk_img

    # Salvar correção
    def salvar_correcao():
        matricula = entry_matricula.get()
        if not matricula.strip():
            messagebox.showwarning(
                "Aviso", "Por favor, preencha a matrícula, a folha e o livro!"
            )
            return

        img_path = img_path_var.get()  # Pega o caminho da imagem enviada
        ocr_text = ocr_text_var.get()  # Pegar o texto ocr gerado antes da correção
        texto_corrigido = text_box.get(
            "1.0", tk.END
        ).strip()  # Pegar o texto corrigido inteiro da caixa

        # Salva esses três no dataframe
        if img_path and texto_corrigido and ocr_text:
            # Pasta para o texto extraído
            os.makedirs("ModeloML/text_ocr", exist_ok=True)
            txt_ocr_path = os.path.join(
                "ModeloML/text_ocr", f"extraido_matricula_{matricula}.txt"
            )

            with open(
                txt_ocr_path,
                "w",
                encoding="utf-8",
            ) as e:
                e.write(ocr_text)

            # Pasta para o texto corrigido
            os.makedirs("ModeloML/transcription", exist_ok=True)
            txt_corrigido_path = os.path.join(
                "ModeloML/transcription", f"corrigido_matricula_{matricula}.txt"
            )

            with open(
                txt_corrigido_path,
                "w",
                encoding="utf-8",
            ) as t:
                t.write(texto_corrigido)

            save_correcao(matricula, img_path, txt_ocr_path, txt_corrigido_path)
            messagebox.showinfo("Sucesso", "Salvos com sucesso!")
        else:
            messagebox.showwarning(
                "Aviso", "Nenhuma imagem ou texto corrigido encontrado."
            )

        # Treinar modelo automaticamente a cada 50 textos corrigidos
        df = pd.read_csv(dfCSV, sep=";", encoding="utf-8")
        total_corrigidos = len(df)

        # Se o número de correções for múltiplo de 50, dispara treino
        if total_corrigidos % 50 == 0 and total_corrigidos > 0:
            messagebox.showwarning("Treinamento", "Executando treino automático...")
            treinar()
        else:
            pass

    # ------------------ Área Widgets --------------------------

    # Botão Upload da Imagem
    botao_upload = customtkinter.CTkButton(
        root,
        text="Upload Imagem",
        command=upload_image,
        cursor="hand2",
        font=("Arial", 12, "bold"),
        height=15,
    )
    botao_upload.grid(row=2, column=0, sticky="nsew", ipadx=5, ipady=5, padx=2, pady=2)

    # Botão do Zoom - Configurar para usar o scroll
    botao_zoom = customtkinter.CTkButton(
        root,
        text="Zoom +",
        command=lambda: zoom_image(1.5),
        cursor="hand2",
        font=("Arial", 12, "bold"),
        height=15,
    )
    botao_zoom.grid(row=3, column=0, sticky="nsew", ipadx=5, ipady=5, padx=2, pady=2)

    botao_correcao = customtkinter.CTkButton(
        root,
        text="Salvar Correção",
        command=salvar_correcao,
        cursor="hand2",
        font=("Arial", 12, "bold"),
        height=15,
        hover_color=("#00125c", "#879100"),
    )
    botao_correcao.grid(
        row=3, column=1, sticky="nsew", ipadx=5, ipady=5, padx=2, pady=2
    )

    root.mainloop()


if __name__ == "__main__":
    app_manuscritIA()
