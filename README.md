## Entregável 2. Anotações de Imagens com OpenCV

Programa desenvolvido em Python para desenhar retângulos sobre imagens a partir de anotações armazenadas em um arquivo CSV.

## Estrutura do projeto

src/main.py: execução principal do programa.
src/modelos.py: classes para representar imagens e detecções.
src/arquivos.py: leitura e organização das anotações.
dados/anotacoes.csv: arquivo com as anotações.
imagens/: imagens originais.
resultados/: imagens anotadas geradas pelo programa.
Requisitos
Python 3
OpenCV
NumPy

## Instale as dependências com:

pip install -r requirements.txt

## Como executar

Na raiz do projeto, execute:

python src/main.py

## Funcionamento

O programa lê as anotações do CSV, valida as coordenadas, desenha retângulos coloridos nas imagens correspondentes e salva os resultados na pasta resultados.
Durante a execução, as imagens são exibidas uma por vez.

Espaço: avança para a próxima imagem.

Q: encerra o programa.

As imagens originais são preservadas.