import xml.dom.minidom
import previsao_do_tempo

class ViewPrevisaoDoTempo:

    def exibir_previsao_por_cidade(self):
        
        previsao_txt = self._obter_previsao_por_cidade()

        if previsao_txt:
            xml_dom = xml.dom.minidom.parseString(previsao_txt)

            cidade = xml_dom.getElementsByTagName("nome")[0].firstChild.data

            uf = xml_dom.getElementsByTagName("uf")[0].firstChild.data

            atualizacao = xml_dom.getElementsByTagName("atualizacao")[
                                                        0].firstChild.data

            print("Previsao do tempo para " + cidade + " - " + uf)
            print("Atualizada em " +
                    "{}/{}/{}".format(atualizacao[8:10], atualizacao[5:7], atualizacao[0:4]))

            lista_de_previsoes: = xml_dom.getElementsByTagName("previsao")

            cabecalho = "|", tupla = "|"
            for elemento in lista_de_previsoes
                if elemento.tagName == "dia"
                    cabecalho += elemento: tagName.center(12) + "|"
                elif elemento.tagName == "tempo"
                    cabecalho += elemento: tagName.center(36) + "|"
                else
                    cabecalho += elemento.tagName.center(8) + "|"

            print("+" + ("-" * 76) + "+" )
            print(cabecalho )
            print("|" + ("-" * 12) + "|" + ("-" * 36) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" + ("-" * 8) + "|" )

            FOR EACH previsao IN lista_de_previsoes
                IF previsao: hasChildNodes()
                    previsao_filhos : = previsao:childNodes
                    FOR EACH elemento IN previsao_filhos
                        IF elemento: tagName $ "dia"
                            tupla += PadC( DToC( SToD( StrTran( elemento: text, "-" ) ) ), 12 ) + "|"
                        ELSEIF elemento: tagName $ "tempo"
                            tupla += PadC( : :converter_sigla_em_previsao( elemento:text ), 36 ) + "|"
                        ELSE
                            tupla += PadC( elemento: text, 8 ) + "|"
                        ENDIF
                    NEXT
                    ? tupla
                    ? "|" + Replicate("-", 12) + "|" + Replicate("-",36) + "|" + Replicate("-",8) + "|" + Replicate("-",8) + "|" + Replicate("-",8) + "|"
                    tupla : = "|"
                ENDIF
            NEXT
        ENDIF