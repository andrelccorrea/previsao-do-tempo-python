import requests
import xml.dom.minidom

def obter_codigo_da_cidade(nome_da_cidade):

    retorno_requisicao = requests.get("http://servicos.cptec.inpe.br/XML/listaCidades", {"city":  nome_da_cidade})

    if retorno_requisicao.status_code == 200:

        if not "<id>" in retorno_requisicao.text:
            print("Nome da cidade nao encontrado!")
            return ""

        documento_xml = xml.dom.minidom.parseString(retorno_requisicao.text)

        codigo_da_cidade = documento_xml.getElementsByTagName("id")[0].firstChild.data

        return codigo_da_cidade

def formatar_data(data_nao_formatada):
    return "{}/{}/{}".format(data_nao_formatada[8:10], data_nao_formatada[5:7], data_nao_formatada[0:4])