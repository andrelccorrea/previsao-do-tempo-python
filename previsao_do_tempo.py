from tabulate import tabulate
import requests
import xml.dom.minidom as minidom

from previsao import Previsao
import uteis

class PrevisaoDoTempo(Previsao):

    # previsão para os próximos 7 dias
    def _obter_previsao(self, nome_da_cidade):

        codigo_da_cidade = self.obter_codigo_da_cidade(nome_da_cidade)

        retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/cidade/7dias/" + codigo_da_cidade + "/previsao.xml")

        if not "<previsao>" in retorno_requisicao.text:
            print("Falha ao obter a previsão!")
            return ""

        return minidom.parseString(retorno_requisicao.text)

    # previsão para os 7 dias posteriores aos próximos 7 dias
    def _obter_previsao_estendida(self, nome_da_cidade):

        codigo_da_cidade = self.obter_codigo_da_cidade(nome_da_cidade)

        retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/cidade/" + codigo_da_cidade + "/estendida.xml")

        if not "<previsao>" in retorno_requisicao.text:
            print("Falha ao obter a previsão!")
            return ""

        return minidom.parseString(retorno_requisicao.text)

    # recebe a previsao em XML e retorna formatada como Dicionário para uso com "tabulate"
    def _converter_previsao_em_dicionario(self, previsao_xml):
        
        previsao_dict = {}

        if previsao_xml:

            previsao_dict["cabecalho"] = [] 
            previsao_dict["linhas"] = []

            previsao_lista = previsao_xml.getElementsByTagName("cidade").item(0).childNodes        
            primeira_iteracao = True
            for previsao in previsao_lista:
                if previsao.tagName == "nome":
                    previsao_dict["cidade"] =  previsao.firstChild.data
                elif previsao.tagName == "uf":
                    previsao_dict["uf"] =  previsao.firstChild.data
                elif previsao.tagName == "atualizacao":
                    previsao_dict["data_da_consulta"] =  previsao.firstChild.data
                else:
                    if previsao.hasChildNodes():
                        previsao_filhos = previsao.childNodes
                        linha = []
                        for elemento in previsao_filhos:
                            if primeira_iteracao:
                                previsao_dict["cabecalho"].append(elemento.tagName)
                            if elemento.tagName == "dia":
                                linha.append( uteis.formatar_data(elemento.firstChild.data))
                            elif elemento.tagName == "tempo":
                                linha.append( self._converter_sigla_da_previsao(elemento.firstChild.data.strip()) )
                            else:
                                linha.append( elemento.firstChild.data )
                        previsao_dict["linhas"].append( linha )
                        primeira_iteracao = False
        
        return previsao_dict

    # converte as siglas retornadas em previsao completa
    def _converter_sigla_da_previsao(self, sigla):

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

    def retornar_previsao(self, nome_da_cidade):
        
        previsao_xml = self._obter_previsao(nome_da_cidade)

        if previsao_xml:    
            previsao_dict = self._converter_previsao_em_dicionario(previsao_xml)

            previsao = "Previsao do tempo para os próximos 7 dias para " + previsao_dict['cidade'] + " - " + previsao_dict['uf'] + "\r\n"
            previsao += "Atualizada em " + uteis.formatar_data(previsao_dict['data_da_consulta']) + "\r\n"
            previsao += tabulate(previsao_dict['linhas'], headers=previsao_dict['cabecalho'])

            return previsao

    def retornar_previsao_estendida(self, nome_da_cidade):
        
        previsao_xml = self._obter_previsao_estendida(nome_da_cidade)

        if previsao_xml:    
            previsao_dict = self._converter_previsao_em_dicionario(previsao_xml)

            previsao = "Previsao do tempo para os 7 dias da próxima semana" + "\r\n"
            previsao += "para " + previsao_dict['cidade'] + " - " + previsao_dict['uf'] + "\r\n"
            previsao += "Atualizada em " + uteis.formatar_data(previsao_dict['data_da_consulta']) + "\r\n"
            previsao += tabulate(previsao_dict['linhas'], headers=previsao_dict['cabecalho'])

            return previsao