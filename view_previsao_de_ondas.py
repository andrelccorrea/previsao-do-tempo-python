import xml.dom.minidom
from previsao_de_ondas import PrevisaoDeOndas

class ViewPrevisaoDeOndas:

    def __init__( self, nome_da_cidade ):
        self.nome_da_cidade = nome_da_cidade
        self.previsao_de_ondas = PrevisaoDeOndas( self.nome_da_cidade )

    def exibir_previsao_do_dia(self):
        previsao_txt = self.previsao_de_ondas._obter_previsao_do_dia()



        return previsao_txt
        
    def exibir_previsao_da_semana(self):
        previsao_txt = self.previsao_de_ondas._obter_previsao_da_semana()



        return previsao_txt
