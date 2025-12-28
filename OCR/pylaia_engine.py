import os
import cv2
from .base import (
    OCREngine,
)  # importou do arquivo base.py com a ajuda do arquivo __init__.py


class PyLaiaEngine(OCREngine):

    def __init__(self, model_path):
        self.model = self.load_model(model_path)

    # Carregar modelo ML
    def load_model(self, model_path):
        # placeholder: aqui entra o modelo PyLaia real
        return None

    # Pré processar a imagem
    def preprocess(self, img_path):
        # Lê a imagem e coloca na escala de tins de cinza
        img = cv2.imread(img_path, cv2.IMREAD_GRAYSCALE)
        # Redimensiona a imagem
        img = cv2.resize(img, None, fx=3, fy=3, interpolation=cv2.INTER_CUBIC) 
        # Aqui configura a imagem adaptando a iluminação e binarizando ela
        img = cv2.adaptiveThreshold(img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY, 31, 15)

        # Renomeação do caminho da imagem e da extensão
        pasta_saida = os.path.join("ModeloML","dados","Treino","img")
        os.makedirs(pasta_saida, exist_ok=True)  # Cria uma pasta se não existir ainda
        nome_base = os.path.splitext(os.path.basename(img_path))[0]  # Separa o nome da extensão (nome.png --> (nome, .png))
        new_path = os.path.join(pasta_saida, f"{nome_base}.png")  # novo caminho da imagem
        cv2.imwrite(new_path, img)

        return img

    # Dividir as linhas
    def segmentar_linha(self, img):
        # Cria uma matrix estrutural retangular(RECT) de proporção de 200x3 pixels para identificar a linha
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (200, 3))
        # Dilata o contorno das letras
        dilated = cv2.dilate(img, kernel, iterations=1)
        # Encontra os contornos externos detectados cada frase/palavra
        # Cada contorno encontrado tende a representar uma linha de texto inteira.
        contorno, _ = cv2.findContours(
            dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
        )
        # Ordenar as linhas de cima para baixo com a função boundingRect que calcula as coordenadas e o tamnho do retângulo isolando as palavras
        linhas = sorted(contorno, key=lambda c: cv2.boundingRect(c)[1])
        return linhas
    
    # Dividir palavras
    def segmentar_palavra(self, img_linha):
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3,25))
        dilated = cv2.dilate(img_linha, kernel, iterations=1)

        contorno, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        palavras = sorted(contorno, key=lambda c: cv2.boundingRect(c)[0])
        return palavras

    # Processar a imagem e extrair texto
    def process_image(self, img_path):
        img = self.preprocess(img_path)
        linhas = self.segmentar_linha(img)

        coord_rect = []
        # Aqui extrai as coordenadas da linha onde está a palavra a ser analisada
        for linha in linhas:
            # Coordenadas na imagem
            x_l, y_l, w_l, h_l = cv2.boundingRect(linha)
            # Imagem da linha recortada
            linha_img = img[y_l: y_l + h_l, x_l: x_l + w_l]

            palavras = self.segmentar_palavra(linha_img)

        # Aqui extrai as coordenadas da palavra a ser analisada na imagem da linha
        for palavra in palavras:
            # Coordenada da palavra
            x_p, y_p, w_p, h_p = cv2.boundingRect(palavra)
            # Coordenadas da palavra na linha
            x_global = x_l + x_p
            y_global = y_l + y_p
            # Imagem da palavra na linha
            palavra_img = img[y_global: y_global + h_p, x_global: x_global + w_p]

            # texto_palavra = self.model.predict(palavra_img)
            texto_palavra = "[Palavra OCR]"  # mock temporário

            # Coordenadas do retângulos que delimitam as linhas/palavras + o texto da linha/palavra
            rects = {"x": x_global, 
                     "y": y_global, 
                     "w": w_p, 
                     "h": h_p, 
                     "texto": texto_palavra}

            coord_rect.append(rects)

        texto_completo = "\n".join([r["texto"] for r in coord_rect])

        return texto_completo, coord_rect
