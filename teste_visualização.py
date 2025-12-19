from PIL import Image
import os

im = Image.open("img-teste\IMG-20251210-WA0007.jpg")

# nova_imagem = im.resize((im.width*3, im.height*3), Image.LANCZOS)

# # Salva com metadado de 300 dpi
# nova_imagem.save("saida_img.png", dpi=(300, 300))


nova_img, ext = os.path.splitext("img-teste\IMG-20251210-WA0007.jpg")


print(nova_img)