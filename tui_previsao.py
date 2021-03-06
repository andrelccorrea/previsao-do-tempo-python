from previsao_do_tempo import PrevisaoDoTempo
from previsao_de_ondas import PrevisaoDeOndas
import os

def main():
    opcao = "N"
    while opcao not in 'Ss':
        opcao = menu()

def menu():
    print("+-----------------------------------------------+")
    print("| Previsão do TEMPO e ONDAS - Fonte: CPTEC/INPE |")
    print("|-----------------------------------------------|")
    print("|  Escolha uma opção e digite o nome da cidade  |")
    print("|                                               |")
    print("|  1 - Tempo para os próximos 7 dias            |")
    print("|  2 - Tempo para os 7 dias posteriores         |")
    print("|  3 - Ondas para o dia atual                   |")
    print("|  4 - Ondas para os próximos 6 dias            |")
    print("|  S - SAIR                                     |")
    print("+-----------------------------------------------+\r\n")
    opcao = input("Opção: ")
    if opcao in "Ss":
        return opcao
    cidade = input("Cidade: ")
    limpar_tela()
    if   opcao in "12":
        previsao = PrevisaoDoTempo()
        if opcao == "1":
            print( previsao.retornar_previsao(cidade) )
        elif opcao == "2":
            print( previsao.retornar_previsao_estendida(cidade) )
    elif opcao in "34":
         previsao = PrevisaoDeOndas(cidade)
         if opcao == "3":
            print( previsao.retornar_previsao_do_dia() )
         elif opcao == "4":
            print( previsao.retornar_previsao_da_semana() )
    else:
        print("Opção inválida.")
    input("\r\nPressione qualquer tecla para continuar...")
    limpar_tela()
    return opcao

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

if __name__ == "__main__":
    main()