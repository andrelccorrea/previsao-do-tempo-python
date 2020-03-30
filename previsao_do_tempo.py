import requests
from uteis import obter_codigo_da_cidade

class PrevisaoDoTempo:

    def __init__(self, nome_da_cidade):
        self._previsao = ""
        self._nome_da_cidade = nome_da_cidade
        self._codigo_da_cidade = obter_codigo_da_cidade(self._nome_da_cidade)

    def _obter_previsao(self):

        if self._codigo_da_cidade:

            retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/cidade/7dias/" + self._codigo_da_cidade + "/previsao.xml")

            if not "<previsao>" in retorno_requisicao.text:
                print("Falha ao obter a previsão!")
                return ""

            return retorno_requisicao.text

    def _obter_previsao_estendida(self):

        if self._codigo_da_cidade:

            retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/estendida.xml")

            if not "<previsao>" in retorno_requisicao.text:
                print("Falha ao obter a previsão!")
                return ""

            return retorno_requisicao.text


    def _converter_sigla_em_previsao(self, sigla):

        previsao = {
            "ec": "Encoberto com Chuvas Isoladas",
            "ci": "Chuvas Isoladas",
            "c": "Chuva",
            "in": "Instável",
            "pp": "Poss. de Pancadas de Chuva",
            "cm": "Chuva pela Manha",
            "cn": "Chuva a Noite",
            "pt": "Pancadas de Chuva a Tarde",
            "pm": "Pancadas de Chuva pela Manha",
            "np": "Nublado e Pancadas de Chuva",
            "pc": "Pancadas de Chuva",
            "pn": "Parcialmente Nublado",
            "cv": "Chuvisco",
            "ch": "Chuvoso",
            "t": "Tempestade",
            "ps": "Predominio de Sol",
            "e": "Encoberto",
            "n": "Nublado",
            "cl": "Ceu Claro",
            "nv": "Nevoeiro",
            "g": "Geada",
            "ne": "Neve",
            "nd": "Nao Definido",
            "pnt": "Pancadas de Chuva a Noite",
            "psc": "Possibilidade de Chuva",
            "pcm": "Possibilidade de Chuva pela Manha",
            "pct": "Possibilidade de Chuva a Tarde",
            "pcn": "Possibilidade de Chuva a Noite",
            "npt": "Nublado com Pancadas a Tarde",
            "npn": "Nublado com Pancadas a Noite",
            "ncn": "Nublado com Poss. de Chuva a Noite",
            "nct": "Nublado com Poss. de Chuva a Tarde",
            "ncm": "Nubl. c/ Poss. de Chuva pela Manha",
            "npm": "Nublado com Pancadas pela Manha",
            "npp": "Nublado com Possibilidade de Chuva",
            "vn": "Variação de Nebulosidade",
            "ct": "Chuva a Tarde",
            "ppn": "Poss. de Panc. de Chuva a Noite",
            "ppt": "Poss. de Panc. de Chuva a Tarde",
            "ppm": "Poss. de Panc. de Chuva pela Manha"
        }

        return previsao.get(sigla, "Sigla não encontrada.")