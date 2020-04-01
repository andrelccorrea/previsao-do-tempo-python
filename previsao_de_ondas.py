import requests
import xml.dom.minidom as minidom

from previsao import Previsao

class PrevisaoDeOndas:
    def __init__( self, nome_da_cidade ):
        self._previsao = ""
        self._codigo_da_cidade = Previsao().obter_codigo_da_cidade(nome_da_cidade)

    def _obter_previsao_do_dia( self ):
        
        if self._codigo_da_cidade:

            retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/dia/0/ondas.xml" )

            if "undefined" in retorno_requisicao.text:
                print( "Falha ao obter a previsão!" )
                return ""

            return minidom.parseString(retorno_requisicao.text)

    def _obter_previsao_da_semana( self ):
        
        if self._codigo_da_cidade:

            retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/todos/tempos/ondas.xml" )  

            if not "<previsao>" in retorno_requisicao.text:
                print( "Falha ao obter a previsão!" )
                return ""

            return minidom.parseString(retorno_requisicao.text)

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
                            
                            if elemento.tagName == "direcao":
                                linha.append( self._converter_sigla_do_ponto_cardeal( elemento.firstChild.data ) )
                            elif elemento.tagName == "vento_dir":
                                linha.append( self._converter_sigla_do_ponto_cardeal( elemento.firstChild.data ) )
                            else:
                                linha.append( elemento.firstChild.data )
                        previsao_dict["linhas"].append( linha )
                        primeira_iteracao = False
        
        return previsao_dict

    def _converter_sigla_do_ponto_cardeal(self, sigla):

        ponto_cardeal = {
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

        return ponto_cardeal.get(sigla, "Sigla não encontrada.")
