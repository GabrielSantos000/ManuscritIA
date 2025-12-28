# Aqui define um padrão para todos os tipos de ferramentas OCR que possam vir no futuro caso eu queira mudar.
# Define o "contrato" que todo OCR sistema deve seguir, garantindo que eu não dependa de bibliotecas
# Essa engenharia de software cria uma interface particular para a ferramenta OCR fazendo com que, caso haja a uma mudança de ferramenta OCR para outra (Pytesseract, Pytorch, ...), eu não precisa recriar tudo novamente, apenas mudar o "motor".

from abc import ABC, abstractmethod

class OCREngine(ABC):
    # Todo OCR do sistema deve saber carregar um modelo ML.
    @abstractmethod
    def load_model(self, model_path):
        pass
    # Todo OCR do sistema deve saber processar as imagens convertendo-as em texto.
    @abstractmethod
    def process_image(self, img_path):
        """
        Processa uma imagem e retorna:
        -> texto OCR completo 
        -> lista de bounding boxes (caixinhas que identica as palavras)
        """
        pass
