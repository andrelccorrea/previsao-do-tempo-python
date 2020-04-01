import requests
import xml.dom.minidom as minidom

from previsao import Previsao
import uteis

class PrevisaoDoTempo(Previsao):

    def __init__(self, nome_da_cidade):

        self._codigo_da_cidade = self.obter_codigo_da_cidade(nome_da_cidade)
        self._link_previsao = "http://servicos.cptec.inpe.br/XML/cidade/7dias/" + self._codigo_da_cidade + "/previsao.xml"
        self._link_previsao_estendida = "http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/estendida.xml"

    # previsão para os próximos 7 dias
    def _obter_previsao(self):

        if self._codigo_da_cidade:

            retorno_requisicao = requests.get(self._link_previsao)

            if not "<previsao>" in retorno_requisicao.text:
                print("Falha ao obter a previsão!")
                return ""

            return minidom.parseString(retorno_requisicao.text)

    # previsão para os 7 dias posteriores aos próximos 7 dias
    def _obter_previsao_estendida(self):

        if self._codigo_da_cidade:

            retorno_requisicao = requests.get(self._link_previsao_estendida)

            if not "<previsao>" in retorno_requisicao.text:
                print("Falha ao obter a previsão!")
                return ""

            return minidom.parseString(retorno_requisicao.text)

    def _retornar_previsao_formatada(self, previsao_xml):
        cidade = previsao_xml.getElementsByTagName("nome")[0].firstChild.data
        uf = previsao_xml.getElementsByTagName("uf")[0].firstChild.data
        atualizacao = previsao_xml.getElementsByTagName("atualizacao")[0].firstChild.data

        texto_previsao = "Previsao do tempo para " + cidade + " - " + uf + "\r\n"
        texto_previsao += "Atualizada em " + uteis.formatar_data(atualizacao) + "\r\n"

        lista_de_previsoes = previsao_xml.getElementsByTagName("previsao")

        cabecalho = "|"
        tupla = "|"

        for elemento in lista_de_previsoes.item(0).childNodes:
            if elemento.tagName == "dia":
                cabecalho += elemento.tagName.center(12) + "|"
            elif elemento.tagName == "tempo":
                cabecalho += elemento.tagName.center(36) + "|"
            else:
                cabecalho += elemento.tagName.center(8) + "|"

        texto_previsao += "+" + ("-" * 76) + "+" + "\r\n"
        texto_previsao += cabecalho + "\r\n"
        texto_previsao += "|" + ("-" * 12) + "|" + ("-" * 36) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" + "\r\n"

        for previsao in lista_de_previsoes:
            if previsao.hasChildNodes():
                previsao_filhos = previsao.childNodes
                for elemento in previsao_filhos:
                    if elemento.tagName == "dia":
                        tupla += uteis.formatar_data(elemento.firstChild.data).center(12) + "|"
                    elif elemento.tagName == "tempo":
                        tupla += self._converter_sigla_em_previsao(elemento.firstChild.data.strip()).center(36) + "|"
                    else:
                        tupla += elemento.firstChild.data.center(8) + "|"
                texto_previsao += tupla  + "\r\n"
                texto_previsao += "|" + ("-" * 12) + "|" + ("-" * 36) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|"  + "\r\n"
                tupla = "|"
        return texto_previsao

    # recebe a previsao em XML e retorna formatada como Dicionário
    def _converter_previsao_em_dicionario(self, previsao_xml):
        
        if previsao_xml:

            # cria o dicionário
            previsao_dict = {}

            # dados iniciais
            previsao_dict["cidade"] = previsao_xml.getElementsByTagName("nome")[0].firstChild.data
            previsao_dict["uf"] = previsao_xml.getElementsByTagName("uf")[0].firstChild.data
            previsao_dict["atualizacao"] = previsao_xml.getElementsByTagName("atualizacao")[0].firstChild.data

            # obtém os elementos "previsao"
            lista_de_previsoes = previsao_xml.getElementsByTagName("previsao")

            # extrai os dados, separando cada previsão em um dicionário numerado a partir de 1
            contador = 1
            for previsao in lista_de_previsoes:
                if previsao.hasChildNodes():
                    previsao_filhos = previsao.childNodes
                    previsao_dict[contador] = {}
                    for elemento in previsao_filhos:
                        previsao_dict[contador][elemento.tagName] = elemento.firstChild.data
                    contador += 1
            return previsao_dict

    # converte as siglas retornadas em previsao completa
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

    def exibir_previsao(self):
        print( self._retornar_previsao_formatada( self._obter_previsao() ) )

    def exibir_previsao_estendida(self):
        print( self._retornar_previsao_formatada( self._obter_previsao_estendida() ) )