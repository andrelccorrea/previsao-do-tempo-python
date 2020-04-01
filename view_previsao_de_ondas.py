from tabulate import tabulate
from previsao_de_ondas import PrevisaoDeOndas

class ViewPrevisaoDeOndas:

    def __init__( self, nome_da_cidade ):
        self._previsao_de_ondas = PrevisaoDeOndas( nome_da_cidade )
        self._cabecalho = []
        self._linhas = []
          
    def exibir_previsao_do_dia(self):

        previsao_xml = self._previsao_de_ondas._obter_previsao_do_dia()
        
        if previsao_xml:
            
            cidade = previsao_xml.getElementsByTagName("nome")[0].firstChild.data
            uf = previsao_xml.getElementsByTagName("uf")[0].firstChild.data
            atualizacao = previsao_xml.getElementsByTagName("atualizacao")[0].firstChild.data
            
            print("Previsao do dia da semana para " + cidade + " - " + uf)
            print("Atualizada em " + atualizacao)

            self._cabecalho = []
            self._linhas = []

            self.extrair_cabecalho(previsao_xml, "manha")
            self.extrair_lista_de_previsoes(previsao_xml, "manha")
            self.extrair_lista_de_previsoes(previsao_xml, "tarde")
            self.extrair_lista_de_previsoes(previsao_xml, "noite")

            print(tabulate(self._linhas, headers=self._cabecalho))
        
    def exibir_previsao_da_semana(self):

        previsao_xml = self._previsao_de_ondas._obter_previsao_da_semana()
        
        if previsao_xml:
            
            cidade = previsao_xml.getElementsByTagName("nome")[0].firstChild.data
            uf = previsao_xml.getElementsByTagName("uf")[0].firstChild.data
            atualizacao = previsao_xml.getElementsByTagName("atualizacao")[0].firstChild.data
            
            print("Previsao de ondas da semana para " + cidade + " - " + uf)
            print("Atualizada em " + atualizacao)
            
            self._cabecalho = []
            self._linhas = []

            self.extrair_cabecalho(previsao_xml, "previsao")
            self.extrair_lista_de_previsoes(previsao_xml, "previsao")

            print(tabulate(self._linhas, headers=self._cabecalho))

    def extrair_cabecalho(self, previsao_xml, nome_da_tag):
        lista_de_previsoes = previsao_xml.getElementsByTagName(nome_da_tag)
        for elemento in lista_de_previsoes.item(0).childNodes:
            if elemento.tagName == "dia":
                self._cabecalho.append( elemento.tagName.center(18) )
            else:
                self._cabecalho.append( elemento.tagName )

    def extrair_lista_de_previsoes(self, previsao_xml, nome_da_tag):
        lista_de_previsoes = previsao_xml.getElementsByTagName(nome_da_tag)
        for previsao in lista_de_previsoes:
            if previsao.hasChildNodes():
                previsao_filhos = previsao.childNodes
                linha = []
                for elemento in previsao_filhos:
                    if elemento.tagName == "direcao":
                        linha.append( self._previsao_de_ondas._converter_sigla_do_ponto_cardeal( elemento.firstChild.data ) )
                    elif elemento.tagName == "vento_dir":
                        linha.append( self._previsao_de_ondas._converter_sigla_do_ponto_cardeal( elemento.firstChild.data ) )
                    else:
                        linha.append( elemento.firstChild.data )
                self._linhas.append( linha )