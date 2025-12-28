import cv2
import numpy as np

# Carregar a imagem (certifique-se de que esteja no mesmo diretório ou forneça o caminho completo)
x = 'matrícula e textos - treinamento\1969.JPG'
imagem = cv2.imread(x, 0) # Carrega em tons de cinza

# Definir o kernel (elemento estruturante) - um quadrado 5x5 neste caso
kernel = np.ones((5,5), np.uint8)

# Aplicar a dilatação
imagem_dilatada = cv2.dilate(imagem, kernel, iterations=1)

# Visualizar o resultado (opcional)
cv2.imshow("Imagem Original", imagem)
cv2.imshow("Imagem Dilatada", imagem_dilatada)
cv2.waitKey(0)
cv2.destroyAllWindows()
