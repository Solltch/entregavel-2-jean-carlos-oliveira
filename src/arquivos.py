import csv
from pathlib import Path

from modelos import Deteccao, ImagemAnotada


def ler_anotacoes(caminho_csv):
    caminho_csv = Path(caminho_csv)

    if not caminho_csv.is_file():
        raise FileNotFoundError(f"Arquivo CSV não encontrado: {caminho_csv}")

    imagens_anotadas = {}

    campos_obrigatorios = {"imagem", "classe_id", "x_min", "y_min", "x_max", "y_max"}

    try:
        with caminho_csv.open("r", encoding="utf-8-sig", newline="") as arquivo:
            leitor = csv.DictReader(arquivo)

            if leitor.fieldnames is None:
                raise ValueError("O CSV está vazio ou não possui cabeçalho.")

            if not campos_obrigatorios.issubset(leitor.fieldnames):
                raise ValueError("O CSV não contém todas as colunas obrigatórias: " + ", ".join(sorted(campos_obrigatorios)))

            for numero_linha, linha in enumerate(leitor, start=2):
                try:
                    nome_imagem = linha["imagem"].strip()

                    if not nome_imagem:
                        raise ValueError("Nome da imagem vazio.")

                    classe_id = int(linha["classe_id"])

                    x_min = int(linha["x_min"])
                    y_min = int(linha["y_min"])
                    x_max = int(linha["x_max"])
                    y_max = int(linha["y_max"])

                    if classe_id not in (0, 1):
                        raise ValueError(f"Classe inválida: {classe_id}")

                    if not (0 <= x_min < x_max and 0 <= y_min < y_max):
                        raise ValueError("Coordenadas inválidas para a caixa.")

                    if nome_imagem not in imagens_anotadas:
                        imagens_anotadas[nome_imagem] = (ImagemAnotada(nome_imagem))

                    deteccao = Deteccao(classe_id, x_min, y_min, x_max, y_max)

                    imagens_anotadas[nome_imagem].adicionar_deteccao(deteccao)

                except (ValueError, TypeError, KeyError) as erro:
                    raise ValueError(f"Erro na linha {numero_linha} do CSV: {erro}") from erro

    except UnicodeDecodeError as erro:
        raise ValueError("Não foi possível ler o CSV como UTF-8.") from erro

    if not imagens_anotadas:
        raise ValueError("O CSV não contém nenhuma anotação.")

    return imagens_anotadas