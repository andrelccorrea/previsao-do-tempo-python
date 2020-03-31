# formata a data para exibir, de "2020-01-01" para "01/01/2020"
def formatar_data(data_nao_formatada):
    return "{}/{}/{}".format(data_nao_formatada[8:10], data_nao_formatada[5:7], data_nao_formatada[0:4])