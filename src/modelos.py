import cv2


class Deteccao:
    def __init__(self, classe_id, x_min, y_min, x_max, y_max):
        self.classe_id = classe_id
        self.x_min = x_min
        self.y_min = y_min
        self.x_max = x_max
        self.y_max = y_max

    def desenhar(self, imagem):
        cores = { 0: (0, 255, 0),  # Verde
                  1: (255, 0, 0)   # Azul em BGR
                }

        cor = cores[self.classe_id]

        cv2.rectangle(imagem, (self.x_min, self.y_min), (self.x_max, self.y_max), cor, 2)


class ImagemAnotada:
    def __init__(self, nome_imagem):
        self.nome_imagem = nome_imagem
        self.deteccoes = []

    def adicionar_deteccao(self, deteccao):
        self.deteccoes.append(deteccao)

    def gerar_imagem(self, imagem_original):
        copia = imagem_original + 0

        for deteccao in self.deteccoes:
            deteccao.desenhar(copia)

        return copia