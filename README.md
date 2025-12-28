
# Sistema de Reconhecimento de Texto Manuscrito Antigo (ManuscritIA)

## Descrição
Esse é um projeto que implementa um sistema de reconhecimento automático de texto (OCR) especializado em imagens de documentos manuscritos antigos, utilizando a biblioteca PyLaia.

## Funcionalidade Principal
- Processa imagens de textos manuscritos históricos, como matrículas de registro de imóveis.
- Utiliza redes neurais profundas para reconhecimento de padrões.
- Converte imagens em texto digital automaticamente.

## Dependências
- PyLaia: Framework de deep learning para reconhecimento de escrita.
- Bibliotecas de processamento de imagem (PIL, OpenCV, etc.).
- Interface usando o CustomTkinter.

## Casos de Uso
- Digitalização de matrículas antigas de registros imobiliários.
- Preservação digital de textos antigos.
- Análise e indexação de manuscritos.
 
## Ideias futuras
- Formatar o texto extraído para um modelo de matrícula pré-estabelecido pelo Cartório e salvar em arquivo doc utilizando a biblioteca Docx.
- Converter esse arquivo Doc em uma imagem no formato tif.

## Como funciona?
Primeiramente, o sistema possui uma interface simples no qual, no lado esquerdo, mostra a imagem que ele vai fazer o upload e no lado direito o texto extraído pela IA (texto OCR). No momento que o texto é extraído, o mesmo é salvo no dataset antes de ser editado para a correção.
Após o texto ser extraído da imagem, o usuário está livre para editar todas as palavras ou frases que o sistema digitou errado e o mesmo lhe ajuda identificando na imagem quais palavras ele tentou decifrar, agilizando assim o processo de correção. Depois de todas as edições no texto, o usuário clica em enviar correção e o mesmo é salvo no dataset.
Assim, com a versão extraída e com a corrigida, é possível que o sistema calcule o seu desempenho e tente melhorar o reconhecimento de caractéres cada vez mais.

@author Gabriel Santos da Silva (leirbag)
@version 1.0
@since 2025
 