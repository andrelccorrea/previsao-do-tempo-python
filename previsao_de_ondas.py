import requests
import xml.dom.minidom as minidom

from tabulate import tabulate
from previsao import Previsao
import uteis

class PrevisaoDeOndas:    
    def __init__(self, nome_da_cidade):
        self._codigo_da_cidade = Previsao().obter_codigo_da_cidade(nome_da_cidade)

    def _obter_previsao_do_dia(self):
        
        if self._codigo_da_cidade:

            retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/dia/0/ondas.xml")

            if "undefined" in retorno_requisicao.text:
                print("Falha ao obter a previsão!")
                return ""

            return minidom.parseString(retorno_requisicao.text)

    def _obter_previsao_da_semana(self):
        
        if self._codigo_da_cidade:

            retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/todos/tempos/ondas.xml")  

            if not "<previsao>" in retorno_requisicao.text:
                print("Falha ao obter a previsão!")
                return ""

            return minidom.parseString(retorno_requisicao.text)

    def _converter_previsao_em_dicionario(self, previsao_xml):
        
        previsao_dict = {}

        previsao_dict["cidade"] = previsao_xml.getElementsByTagName("nome")[0].firstChild.data
        previsao_dict["uf"] = previsao_xml.getElementsByTagName("uf")[0].firstChild.data
        previsao_dict["atualizacao"] = previsao_xml.getElementsByTagName("atualizacao")[0].firstChild.data
        
        previsao_dict["cabecalho"] = [] 
        previsao_dict["linhas"] = []

        previsao_lista = previsao_xml.getElementsByTagName("cidade").item(0).childNodes        
        primeira_iteracao = True

        for previsao in previsao_lista:
            if previsao.tagName in "manha;tarde;noite;previsao":
                previsao_filhos = previsao.childNodes
                linha = []
                for elemento in previsao_filhos:
                    if primeira_iteracao:
                        previsao_dict["cabecalho"].append(elemento.tagName)                            
                    if elemento.tagName == "direcao":
                        linha.append(self._converter_sigla_do_ponto_cardeal(elemento.firstChild.data))
                    elif elemento.tagName == "vento_dir":
                        linha.append(self._converter_sigla_do_ponto_cardeal(elemento.firstChild.data))
                    elif elemento.tagName == "dia": 
                        linha.append(elemento.firstChild.data.replace("-","/"))
                    else:
                        linha.append(elemento.firstChild.data)
                previsao_dict["linhas"].append(linha)
                primeira_iteracao = False
        
        return previsao_dict

    def _converter_sigla_do_ponto_cardeal(self, sigla):

        pontos_cardeais = {
            "N": "Norte",
            "NNE": "Nor-Nordeste",
            "NE": "Nordeste",
            "ENE": "Leste-Nordeste",
            "E": "Leste",
            "ESE": "Leste-Sudeste",
            "SE": "Sudeste",
            "SSE": "Sul-Sudeste",
            "S": "Sul",
            "SSW": "Sul-Sudoeste",
            "SW": "Sudoeste",
            "WSW": "Oeste-Sudoeste",
            "W": "Oeste",
            "WNW": "Oeste-Noroeste",
            "NW": "Noroeste",
            "NNW": "Noroeste"
        }

        return pontos_cardeais.get(sigla, "Sigla não encontrada.")

    def retornar_previsao_do_dia(self):

        previsao_xml = self._obter_previsao_do_dia()

        if previsao_xml:    
            previsao_dict = self._converter_previsao_em_dicionario(previsao_xml)

            previsao = "Previsao de ondas do dia para " + previsao_dict['cidade'] + " - " + previsao_dict['uf'] + "\r\n"
            previsao += "Atualizada em " + previsao_dict['atualizacao'].replace("-","/") + "\r\n"
            
            previsao += tabulate(previsao_dict['linhas'], headers=previsao_dict['cabecalho'], tablefmt="simple")

            return previsao
        
    def retornar_previsao_da_semana(self):

        previsao_xml = self._obter_previsao_da_semana()  

        if previsao_xml:

            previsao_dict = self._converter_previsao_em_dicionario(previsao_xml)

            previsao = "Previsao de ondas da semana para " + previsao_dict['cidade'] + " - " + previsao_dict['uf'] + "\r\n"
            previsao += "Atualizada em " + uteis.formatar_data( previsao_dict['atualizacao'] ) + "\r\n"
            
            previsao += tabulate(previsao_dict['linhas'], headers=previsao_dict['cabecalho'], tablefmt="simple")

            return previsao