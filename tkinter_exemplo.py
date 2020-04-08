import tkinter as tk
from tkinter import ttk
from tkinter import tix

from previsao_do_tempo import PrevisaoDoTempo
from previsao_de_ondas import PrevisaoDeOndas

# classe Application é herdeira da classe tk.Frame
class Application(tk.Frame):
    def __init__(self, master=None):
        
        # inicializa a classe Pai (Tk.Frame) passando o container principal como argumento
        super().__init__(master)
        
        # define o container principal para toda a aplicação
        #  quando um widget não tem o container pai definido,
        #  assume master como sendo o container principal
        self.master = master
        
        # título da janela
        self.master.title("Previsão do TEMPO e ONDAS - Fonte: CPTEC/INPE")

        # cria os widgets e define as variaveis
        self.opcao    = self.criar_widget_opcao()
        self.cidade   = self.criar_widget_cidade()
        self.previsao = self.criar_widget_previsao()
        self.criar_widget_sair()

    def criar_widget_opcao(self):
        # cria o label    
        label = tk.Label(self.master,   # container
                         text="Opção:") # texto do label
        # posição do label
        label.grid(row=0,  # posição vertical na janela
                   padx=5, # padding horizontal
                   pady=5) # padding vertical
        # lista com as opções
        opcoes = ['Tempo para os próximos 7 dias',
                  'Tempo para os 7 dias posteriores',
                  'Ondas para o dia atual',
                  'Ondas para os próximos 6 dias']
        # cria o combobox
        combobox_opcao = ttk.Combobox(self.master,      # container
                                      state='readonly', # estado do combobox
                                      values=opcoes,    # opções disponíveis
                                      width=30)         # largura
        # define a opção inicial
        combobox_opcao.current(0)
        # define a posição
        combobox_opcao.grid(column=1, # posição horizontal na janela, 2a coluna
                            row=0)    # posição vertical na janela, 1a linha
        return combobox_opcao

    def criar_widget_cidade(self):
        # cria o label
        label = tk.Label(self.master,     # container
                         text="Cidade:")  # texto do label
        # posição do label
        label.grid(row=1,  # posição vertical na janela
                   padx=5, # padding horizontal
                   pady=5) # padding vertical
        # cria o edit
        entry = tk.Entry(self.master, #container
                         width=30)    # tamanho do campo
        # define a posição do widget
        entry.grid(column=1, # posição horizontal na janela, 2a coluna
                   row=1)    # posição vertical na janela, 2a linha
        # vincula a tecla ENTER ao método exibir_previsao
        entry.bind("<Return>", self.exibir_previsao)

        return entry

    def criar_widget_previsao(self):
        # cria o label
        label = tk.Label(self.master, # container
                         width=70)  # largura em medida de texto)
        # posição do label
        label.grid(column=1,  # posição horizontal na janela, 3a coluna
                   row=5,     # posição vertical na janela
                   padx=5,    # padding horizontal
                   pady=5)    # padding vertical

        return label
    
    def exibir_previsao(self, event=None):
        # obtém a opção do combobox
        opcao = self.opcao.current() # current() retorna o índice
        if opcao   == 0:
            previsao = PrevisaoDoTempo().retornar_previsao(self.cidade.get())
        elif opcao == 1:
            previsao = PrevisaoDoTempo().retornar_previsao_estendida(self.cidade.get())
        elif opcao == 2:
            previsao = PrevisaoDeOndas(self.cidade.get()).retornar_previsao_do_dia()
        elif opcao == 3:
            previsao = PrevisaoDeOndas(self.cidade.get()).retornar_previsao_da_semana()
        
        # carrega os dados da previsão
        self.previsao["text"] = previsao

    def criar_widget_sair(self):
        # cria o botão
        button = tk.Button(self.master,                 # container
                           text="Sair",                 # texto no botão 
                           command=self.master.destroy) # evento
        # posição
        button.grid(column=7, # posição horizontal na janela, 3a coluna
                    row=11,   # posição vertical na janela, 3a linha
                    padx=5,   # padding horizontal
                    pady=5)   # padding vertical

# cria o container principal da aplicação
root = tk.Tk()
# instancia a aplicação
app = Application(master=root)
# loop de execução
app.mainloop()