import requests

from uteis import obter_codigo_da_cidade

class PrevisaoDeOndas:
    def __init__( self, nome_da_cidade ):
        self.previsao = ""
        self.nome_da_cidade = nome_da_cidade
        self.codigo_da_cidade = obter_codigo_da_cidade( self.nome_da_cidade )

    def _obter_previsao_do_dia( self ):
        
        if self.codigo_da_cidade:

            retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/cidade/" + self.codigo_da_cidade + "/dia/0/ondas.xml" )

            print("http://servicos.cptec.inpe.br/XML/cidade/" + self.codigo_da_cidade + "/dia/0/ondas.xml")

            if "undefined" in retorno_requisicao.text:
                print( "Falha ao obter a previsão!" )
                return None

            return retorno_requisicao.text

    def _obter_previsao_da_semana( self ):
        
        if self.codigo_da_cidade:

            retorno_requisicao = requests.get( "http://servicos.cptec.inpe.br/XML/cidade/" + self.codigo_da_cidade + "/todos/tempos/ondas.xml" )  

            if not "<previsao>" in retorno_requisicao.text:
                print( "Falha ao obter a previsão!" )
                return None

            return retorno_requisicao.text