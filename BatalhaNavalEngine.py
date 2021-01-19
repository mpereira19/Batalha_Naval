# -*- coding:utf-8 -*-
'''
Created on 28/10/2019

@author: valves
'''


class BatalhaNavalEngine:

    def __init__(self):
        self.tab_jogo = []  # matriz que representa o tabuleiro de jogo original
        self.tab_estado = []  # matriz que representa o tabuleiro com o estado do jogo
        self.jogador = "top_gun"
        self.score = 0
    
    def ler_tabuleiro_ficheiro(self, filename):
        '''
        Cria nova instancia do jogo numa matriz
        :param filename: nome do ficheiro a ler
        como o formato é fixo sabe-se o que contem cada linha
        '''
        try:
            ficheiro = open(filename, "r")
            lines = ficheiro.readlines()  # ler as linhas do ficheiro para a lista lines
            self.tab_jogo = []
            for i in range(1, 11):  # as linhas 1 a 11 contêm o tabuleiro de jogo
                self.tab_jogo.append(lines[i].split())
            self.tab_estado = []
            for i in range(12, 22):
                self.tab_estado.append(lines[i].split())
            estado = True
            self.score = int(lines[23])
        except:
            print("Erro: na leitura do tabuleiro")
            estado = False
        else:
            ficheiro.close()
        return estado
    
    def print_tab_jogo(self):
        print("  1 2 3 4 5 6 7 8 9 10")
        letras = ['A','B','C','D','E','F','G','H','I','J']
        i = 0
        for linha in self.tab_jogo:
            print(letras[i], end=" ")
            i += 1
            for simbolo in linha:
                print(simbolo, end=" ")
            print()
        print("[%s] Jogadas efetuadas:%d"%(self.jogador, self.score))
        
    def print_tab_estado(self):
        print("\n  1 2 3 4 5 6 7 8 9 10")
        letras=['A','B','C','D','E','F','G','H','I','J']
        i = 0
        for linha in self.tab_estado:
            print(letras[i], end=" ")
            i += 1
            for simbolo in linha:
                print(simbolo, end=" ")
            print()
        print("[%s] Jogadas efetuadas:%d" % (self.jogador, self.score))

    def setjogador(self,jog):
        self.jogador = jog
    
    def getjogador(self):
        return self.jogador
    
    def gettab_estado(self):
        return self.tab_estado

    def settab_estado(self, t):
        self.tab_estado = t
