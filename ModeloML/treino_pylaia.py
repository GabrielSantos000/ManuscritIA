import subprocess

cmd = [
    "python",  # Executar o pyhton
    "-m",  # Roda o módulo a seguir
    "pylaia.train",  # Módulo de treinamento do próprio PyLaia
    "--train_img",  # Imagem para o treinamento
    "ModeloML\\dados\\Treino\\img",  # Que estão nessa pasta
    "--train_txt",  # Transcrição corrigida para treinamento
    "ModeloML\\dados\\Treino\\transcription",  # Que estão nessa pasta
    "--val_img",  # Imagem validada
    "ModeloML\\dados\\validacao\\img",  # Que estão nessa pasta
    "--val_txt",  # Transcrição validada
    "ModeloML\\dados\\validacao\\transcription",  # Que estão nessa pasta
    "--output",  # saída do
    "ModeloML\\modelos\\pylaia",  # Modelo de treinamento
    "--epochs",  # época: define quantas vezes a IA é treinada
    "20",  # A cada x transcrições feitas
    "--batch_size",  # Deifine a quantidade de imagens que o modelo processa de uma vez
    "4",  # 4 imagens
]

subprocess.run(cmd)
