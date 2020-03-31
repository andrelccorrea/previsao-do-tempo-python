import xml.dom.minidom
from previsao_do_tempo import PrevisaoDoTempo
import uteis

class ViewPrevisaoDoTempo:

    def __init__(self, nome_da_cidade):
        self.previsao_do_tempo = PrevisaoDoTempo(nome_da_cidade)

    def exibir_previsao(self):
        
        previsao_txt = self.previsao_do_tempo._obter_previsao()
        self.processar_previsao(previsao_txt)

    def exibir_previsao_estendida(self):
        previsao_txt = self.previsao_do_tempo._obter_previsao_estendida()
        self.processar_previsao(previsao_txt)

    def processar_previsao(self, previsao_txt):

        if previsao_txt:
            xml_dom = xml.dom.minidom.parseString(previsao_txt)

            cidade = xml_dom.getElementsByTagName("nome")[0].firstChild.data

            uf = xml_dom.getElementsByTagName("uf")[0].firstChild.data

            atualizacao = xml_dom.getElementsByTagName("atualizacao")[0].firstChild.data

            print("Previsao do tempo para " + cidade + " - " + uf)
            print("Atualizada em " + uteis.formatar_data(atualizacao))

            lista_de_previsoes = xml_dom.getElementsByTagName("previsao")

            cabecalho = "|"
            tupla = "|"

            for elemento in lista_de_previsoes.item(0).childNodes:
                if elemento.tagName == "dia":
                    cabecalho += elemento.tagName.center(12) + "|"
                elif elemento.tagName == "tempo":
                    cabecalho += elemento.tagName.center(36) + "|"
                else:
                    cabecalho += elemento.tagName.center(8) + "|"

            print("+" + ("-" * 76) + "+" )
            print(cabecalho)
            print("|" + ("-" * 12) + "|" + ("-" * 36) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" )

            for previsao in lista_de_previsoes:
                if previsao.hasChildNodes():
                    previsao_filhos = previsao.childNodes
                    for elemento in previsao_filhos:
                        if elemento.tagName == "dia":
                            tupla += uteis.formatar_data(elemento.firstChild.data).center(12) + "|"
                        elif elemento.tagName == "tempo":
                            tupla += self.previsao_do_tempo._converter_sigla_em_previsao(elemento.firstChild.data.strip()).center(36) + "|"
                        else:
                            tupla += elemento.firstChild.data.center(8) + "|"
                    print(tupla)
                    print("|" + ("-" * 12) + "|" + ("-" * 36) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" )
                    tupla = "|"