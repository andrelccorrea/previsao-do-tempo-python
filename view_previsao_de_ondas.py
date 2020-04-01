from tabulate import tabulate
from previsao_de_ondas import PrevisaoDeOndas

import uteis

class ViewPrevisaoDeOndas:

    def __init__( self, nome_da_cidade ):
        self._previsao_de_ondas = PrevisaoDeOndas( nome_da_cidade )
          
    def exibir_previsao_do_dia(self):

        previsao_xml = self._previsao_de_ondas._obter_previsao_do_dia()

        if previsao_xml:    
            previsao_dict = self._previsao_de_ondas._converter_previsao_em_dicionario(previsao_xml)

            print("Previsao de ondas do dia para " + previsao_dict['cidade'] + " - " + previsao_dict['uf'])
            print("Atualizada em " + previsao_dict['data_da_consulta'])
            
            print(tabulate(previsao_dict['linhas'], headers=previsao_dict['cabecalho']))
        
    def exibir_previsao_da_semana(self):

        previsao_xml = self._previsao_de_ondas._obter_previsao_da_semana()
        
        if previsao_xml:
            previsao_dict = self._previsao_de_ondas._converter_previsao_em_dicionario(previsao_xml)

            print("Previsao de ondas da semana para " + previsao_dict['cidade'] + " - " + previsao_dict['uf'])
            print("Atualizada em " + previsao_dict['data_da_consulta'])
            
            print(tabulate(previsao_dict['linhas'], headers=previsao_dict['cabecalho']))

    