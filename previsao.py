import requests
import xml.dom.minidom as minidom

class Previsao:
    # recebe o nome ou parte do nome de uma cidade e retorna o código usado nas consultas
    def obter_codigo_da_cidade(self, nome_da_cidade):

        retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/listaCidades", {"city": nome_da_cidade})

        if retorno_requisicao.status_code == 200:

            if not "<id>" in retorno_requisicao.text:
                print("Nome da cidade nao encontrado!")
                return ""

            documento_xml = minidom.parseString(retorno_requisicao.text)

            codigo_da_cidade = documento_xml.getElementsByTagName("id")[0].firstChild.data

            return codigo_da_cidade