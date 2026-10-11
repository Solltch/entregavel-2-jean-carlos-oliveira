import cv2
import numpy as np
from pathlib import Path

from arquivos import ler_anotacoes

def ler_imagem(caminho):
    dados = np.fromfile(str(caminho), dtype=np.uint8)
    imagem = cv2.imdecode(dados, cv2.IMREAD_COLOR)
    return imagem

def salvar_imagem(caminho, imagem):
    try:
        sucesso, dados = cv2.imencode(".jpg", imagem)

        if not sucesso:
            print("Erro: o OpenCV não conseguiu codificar a imagem.")
            return False

        dados.tofile(str(caminho))

        if not caminho.is_file() or caminho.stat().st_size == 0:
            print("Erro: o arquivo não foi gravado corretamente.")
            return False

        return True

    except Exception as erro:
        print(f"Erro detalhado ao salvar a imagem: {erro}")
        return False



RAIZ = Path(__file__).resolve().parent.parent

PASTA_IMAGENS = RAIZ / "imagens"
PASTA_DADOS = RAIZ / "dados"
PASTA_RESULTADOS = RAIZ / "resultados"

CAMINHO_CSV = PASTA_DADOS / "anotacoes.csv"


def validar_coordenadas(imagem, nome_imagem, imagem_anotada):
    altura, largura = imagem.shape[:2]

    for numero, deteccao in enumerate(imagem_anotada.deteccoes, start=1):
        if not (0 <= deteccao.x_min < deteccao.x_max < largura and 0 <= deteccao.y_min < deteccao.y_max < altura):
            raise ValueError(
                f"Coordenadas inválidas na imagem {nome_imagem}, "
                f"caixa {numero}. "
                f"Dimensões: {largura}x{altura}; "
                f"caixa: ({deteccao.x_min}, {deteccao.y_min}) "
                f"até ({deteccao.x_max}, {deteccao.y_max})."
                )


def adicionar_legenda(imagem, nome_imagem):
    altura, largura = imagem.shape[:2]

    cv2.putText(imagem,  nome_imagem, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2, cv2.LINE_AA)

    cv2.putText(imagem, "Classe 0", (10, altura - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2, cv2.LINE_AA)

    cv2.putText(imagem, "Classe 1", (130, altura - 35), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 0, 0), 2, cv2.LINE_AA)


def preparar_exibicao(imagem, largura_maxima=1200, altura_maxima=800):
    altura, largura = imagem.shape[:2]

    escala = min(largura_maxima / largura, altura_maxima / altura, 1.0)

    if escala < 1.0:
        nova_largura = int(largura * escala)
        nova_altura = int(altura * escala)

        return cv2.resize(imagem, (nova_largura, nova_altura), interpolation=cv2.INTER_AREA)

    return imagem


def main():
    if not PASTA_IMAGENS.is_dir():
        raise FileNotFoundError(f"Pasta de imagens não encontrada: {PASTA_IMAGENS}")

    PASTA_RESULTADOS.mkdir(parents=True, exist_ok=True)

    imagens_anotadas = ler_anotacoes(CAMINHO_CSV)

    nomes_imagens = sorted(arquivo.name for arquivo in PASTA_IMAGENS.iterdir() if arquivo.is_file() and arquivo.suffix.lower() in (".jpg", ".jpeg"))

    if len(nomes_imagens) != 10:
        raise ValueError(f"Esperadas 10 imagens JPG, mas foram encontradas " f"{len(nomes_imagens)}.")

    for nome in imagens_anotadas:
        if nome not in nomes_imagens:
            raise FileNotFoundError(f"A imagem {nome} está no CSV, mas não foi encontrada " f"na pasta {PASTA_IMAGENS}.")

    cv2.namedWindow("Visualizador de imagens anotadas", cv2.WINDOW_NORMAL)

    try:
        for nome_imagem in nomes_imagens:
            caminho_imagem = PASTA_IMAGENS / nome_imagem

            imagem_original = ler_imagem(caminho_imagem)

            if imagem_original is None:
                raise ValueError(f"Não foi possível abrir a imagem: {caminho_imagem}")

            anotacoes = imagens_anotadas.get(nome_imagem)

            if anotacoes is None:
                from modelos import ImagemAnotada
                anotacoes = ImagemAnotada(nome_imagem)

            validar_coordenadas(imagem_original, nome_imagem, anotacoes)

            imagem_final = anotacoes.gerar_imagem(imagem_original)
            adicionar_legenda(imagem_final, nome_imagem)

            caminho_resultado = PASTA_RESULTADOS / nome_imagem

            if not salvar_imagem(caminho_resultado, imagem_final):
                raise OSError(f"Não foi possível salvar: {caminho_resultado}")

            quantidade = len(anotacoes.deteccoes)

            print(f"Imagem: {nome_imagem} | " f"Caixas desenhadas: {quantidade}")

            imagem_exibicao = preparar_exibicao(imagem_final)

            cv2.imshow("Visualizador de imagens anotadas", imagem_exibicao)

            while True:
                tecla = cv2.waitKey(0) & 0xFF

                if tecla == ord("q"):
                    print("Execução encerrada pelo usuário.")
                    return

                if tecla == ord(" "):
                    break

        print("Todas as imagens foram processadas.")
        print(f"Resultados salvos em: {PASTA_RESULTADOS}")

    finally:
        cv2.destroyAllWindows()


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError) as erro:
        print(f"Erro: {erro}")