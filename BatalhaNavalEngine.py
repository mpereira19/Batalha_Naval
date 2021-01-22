# -*- coding:utf-8 -*-
"""
Created on 28/10/2019

@author: valves
"""


class BatalhaNavalEngine:

    def __init__(self):
        self.tab_jogo = []  # matriz que representa o tabuleiro de jogo original
        self.tab_estado = []  # matriz que representa o tabuleiro com o estado do jogo
        self.jogador = "top_gun"
        self.score = 0
        self.plays = 'jogadas.txt'
    
    def ler_tabuleiro_ficheiro(self, filename):
        """
        Cria nova instância do jogo numa matriz
        :param filename: nome do ficheiro a ler
        como o formato é fixo sabe-se o que contem cada linha
        """

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
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        i = 0
        for linha in self.tab_jogo:
            print(letras[i], end=" ")
            i += 1
            for simbolo in linha:
                print(simbolo, end=" ")
            print()
        print("[%s] Jogadas efetuadas: %d" % (self.jogador, self.score))
        
    def print_tab_estado(self):
        print("\n  1 2 3 4 5 6 7 8 9 10")
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        i = 0
        for linha in self.tab_estado:
            print(letras[i], end=" ")
            i += 1
            for simbolo in linha:
                print(simbolo, end=" ")
            print()
        print("[%s] Jogadas efetuadas: %d" % (self.jogador, self.score))

    def setjogador(self, jog):
        self.jogador = jog
    
    def getjogador(self):
        return self.jogador
    
    def gettab_estado(self):
        return self.tab_estado

    def settab_estado(self, t):
        self.tab_estado = t

    def create_jogadas_history(self):
        """
        Função que cria um documento onde serão guardados todos os movimentos.

        Returns
        -------
        None.

        """

        file = open(self.plays, 'w')
        file.write(str(self.tab_estado))
        file.close()

    def add_move(self):
        """
        Função que ao ser chamada acrescenta esse movimento ao ficheiro dos movimentos.

        Returns
        -------
        None.

        """

        file = open(self.plays, 'a')
        file.writelines('\n' + str(self.tab_estado))
        file.close()

    def undo_move(self):
        """
        Função que ao ser chamada retrocede um movimento do jogo.

        Returns
        -------
        None.

        """

        import ast
        file = open(self.plays, 'r')
        lines = file.readlines()
        file1 = open(self.plays, 'w')
        for line in lines:
            if line.strip('\n') != str(self.tab_estado):
                file1.write(line)
        file.close()
        file1.close()

        file = open(self.plays, 'r')
        move = file.readlines()
        file.close()
        last_move = ast.literal_eval(move[len(move)-1])
        self.settab_estado(last_move)

    def add_score(self):
        self.score += 1

    def score_files(self):
        """
        Função que guarda no documento 'Score.txt' todos os scores e jogador que jogaram a batalha naval.

        Returns
        -------
        None.

        """

        import os
        try:
            if os.path.exists('Score.txt') is False:
                file = open('Score.txt', 'w')
                file.write('Scores:\n')
                file.write(f'{self.getjogador()}  {self.score}')

            elif os.path.exists('Score.txt') is True:
                file1 = open('Score.txt', 'r')
                data = file1.readlines()[1:]
                file1.close()
                data1 = [line.replace('\n', '').split() for line in data]
                dic = {line[0]: int(line[1]) for line in data1}
                if self.jogador in list(dic):
                    if self.score < dic[self.jogador]:
                        dic[self.jogador] = self.score
                else:
                    dic[self.jogador] = self.score
                key = list(dic)
                file = open('Score.txt', 'w')
                file.write('Scores:\n')
                for k in key:
                    if k != key[-1]:
                        file.write(f'{k}  {val}\n')
                    else:
                        file.write(f'{k}  {val}')
        except:
            print('Erro em guardar score!!!')

        else:
            file.close()
