# Interface
import tkinter as tk
from tkinter import filedialog, messagebox
from ttkbootstrap.constants import *
import customtkinter

# Reconhecimento e transcrição de textos manuscritos
from OCR.pylaia_engine import PyLaiaEngine

# Importação e leitura de imagens
from PIL import Image, ImageTk

# Leitura e processamentos do dataframe
import pandas as pd

# Acesso ao sistema do computador
import os
import subprocess

# ---------------------------------------------------

# Caminho do dataframe
dfCSV = "ModeloML\dfnovo.csv"

# Criar um dataframe CSV se não existir
if not os.path.exists(dfCSV):
    pd.DataFrame(
        columns=["matricula", "img_path", "texto_corrigido", "ocr_text"]
    ).to_csv(dfCSV, index=False, sep=";", encoding="utf-8")
# ---------------------------------------------------
model_path = os.path.join("ModeloML", "modelos", "pylaia", "modelo.pth")

OCR = PyLaiaEngine(model_path)


# Função para salvar a correção no dataframe
def save_correcao(matricula, img_path, txt_ocr_path, txt_corrigido_path):
    # Lê, adiciona e atualiza
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


# Interface
def app_manuscritIA():
    root = customtkinter.CTk()
    root.title("ManuscritIA - Transcrição Automática de Manuscritos")
    root.iconbitmap("diversos\logo_sistema.ico")
    root.geometry("1200x600")  # Largura x Altura em pixels

    # ---------------- DESIGN E ORGANIZAÇÃO LAYOUT ------------------------------

    customtkinter.set_default_color_theme("dark-blue")

    # Lugar da imagem com o canvas
    canvas = tk.Canvas(root, bg="black")
    canvas.grid(row=1, column=0, sticky="nsew")

    # Definição do grid da janela principal
    root.grid_rowconfigure(0, weight=0)
    root.grid_rowconfigure(1, weight=2)
    root.grid_rowconfigure(2, weight=0)
    root.grid_rowconfigure(3, weight=0)
    root.grid_columnconfigure(0, weight=2)
    root.grid_columnconfigure(1, weight=2)

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

    img_box = customtkinter.CTkLabel(root)
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
                # Transcreve o texto da imagem e armazena na variável texto e armazena as coordenadas do delimitador das palavras
                texto, rects = OCR.process_image(file_path)

                text_box.delete("1.0", tk.END)  # Apaga todo conteúdo da caixa de texto
                text_box.insert(tk.END, texto)  # Adiciona o texto gerado pela OCR
                img_path_var.set(file_path)  # Guarda o caminho da imagem selecionada
                ocr_text_var.set(texto)  # Guarda o texto lido pela IA

                # Exibe imagem com redimensionamento
                im = Image.open(file_path)
                orig_w, orig_h = im.size  # Extrae o tamanho da imagem original

                MAX_W, MAX_H = 1000, 1500
                new_im = im.copy()
                new_im.thumbnail((MAX_W, MAX_H))
                new_w, new_h = new_im.size

                # Redimensionar imagem
                sclx = new_w / orig_w  # Escala x
                scly = new_h / orig_h  # EScala y

                tk_img = ImageTk.PhotoImage(new_im)

                canvas.delete(
                    "all"
                )  # Limpar o canva para não ficar com sobreposição de imagens
                canvas.image = tk_img
                canvas.create_image(0, 0, anchor="nw", image=tk_img)

                def click_box(idx):
                    palavra = rects[idx]["texto"]
                    # text_box.delete("1.0", tk.END)
                    text_box.insert(tk.END, palavra)

                for idx, rect in enumerate(rects):
                    x = int(rect["x"] * sclx)
                    y = int(rect["y"] * scly)
                    w = int(rect["w"] * sclx)
                    h = int(rect["h"] * scly)

                    rectID = canvas.create_rectangle(
                        x, y, x + w, y + h, outline="red", width=2
                    )

                    canvas.tag_bind(
                        rectID,  # ID do retãngulo
                        "<Button-1>",  # Botão esquerdo do mouse
                        lambda e, i=idx: click_box(i),
                    )  # Função a ser aplicada

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
            subprocess.Popen(["python", "ModeloML/prepare_dataset.py"])
            subprocess.Popen(["python", "ModeloML/treino_pylaia.py"])

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
