import requests
import xml.dom.minidom as minidom

from previsao_do_tempo import PrevisaoDoTempo

class PrevisaoDeOndas:
    def __init__( self, nome_da_cidade ):
        self._previsao = ""
        self._codigo_da_cidade = PrevisaoDoTempo(nome_da_cidade)._obter_codigo_da_cidade()

    def _obter_previsao_do_dia( self ):
        
        if self._codigo_da_cidade:

            retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/dia/0/ondas.xml" )

            print("http://servicos.cptec.inpe.br/XML/cidade/" + self._codigo_da_cidade + "/dia/0/ondas.xml")

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

    def _converter_sigla_do_ponto_cardeal(self, sigla):

        previsao = {
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

        return previsao.get(sigla, "Sigla não encontrada.")
