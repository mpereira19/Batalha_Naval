# -*- coding:utf-8 -*-
'''
Created on 28/10/2019

@author: valves
'''
from cmd import *
from BatalhaNavalWindow import BatalhaNavalWindow
from BatalhaNavalEngine import BatalhaNavalEngine


class BatalhaNavalShell(Cmd):
    intro = 'Interpretador de comandos para a Batalha Naval adaptada. Escrever help ou ? para listar os comandos disponíveis.\n'
    prompt = 'BatalhaNaval> '

    players_score = dict()

    def do_jogar(self, arg):
        " -  comando jogar que leva como parâmetro o nome de um ficheiro e a identificação do jogador e carrega o tabuleiro permitindo jogá-lo..: jogar <nome_ficheiro> <jogador> \n" 
        try:
            lista_arg = arg.split()
            num_args = len(lista_arg)
            if num_args == 2:
                eng.ler_tabuleiro_ficheiro(lista_arg[0])
                eng.setjogador(lista_arg[1])
                # eng.print_tab_jogo()
                eng.print_tab_estado()
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao mostrar o puzzle")

    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro e permite gravar o estado do jogo atual..: gravar <nome_ficheiro>  \n"
        try:
            ficheiro = open(arg+'.txt', 'w')
            ficheiro.writelines('Tabuleiro:')
            for lines in range(len(eng.tab_jogo)):
                ficheiro.writelines(*eng.tab_jogo[lines])
            ficheiro.writelines('Estado do Jogo:')
            for lines in range(len(eng.tab_estado)):
                ficheiro.writelines(*eng.tab_estado[lines])
            ficheiro.writelines('Jogadas efetuadas:')
            ficheiro.writelines(eng.score)
            estado = True
        except:
            print('Erro ao guardar o tabuleiro!')
            estado = False
        else:
            ficheiro.close()
        return estado
    
    def do_tiro(self, arg):
        " - comando tiro que leva como parâmetros a linha e a coluna de uma casa onde se pretende jogar..: tiro <l> <c>\n"
        loc = arg.split()
        eng.score += 1
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        if eng.tab_jogo[letras.index(loc[0])][int(loc[1]-1)] == '.':
            eng.tab_estado[letras.index(loc[0])][int(loc[1] - 1)] == 'O'

        pass

    def do_agua(self, arg):
        " - comando que leva como parâmetros a linha e a coluna de uma casa, pertencente a uma embarcação já afundada (totalmente descoberta) que se pretende rodear de “água”..: agua <l> <c> \n"
        pass

    def do_linha(self, arg):
        " - comando linha que permite colocar o estado de todas as casas da linha l que ainda não estão determinadas como sendo “água”...: linha <l> \n"
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        if arg in letras:
            eng.score += 1
            matrix = eng.tab_estado
            for a in range(len(matrix)):
                if matrix[letras.index(arg)][a] == 'X' or matrix[letras.index(arg)][a] == '*' or matrix[letras.index(arg)][a] == 'O': pass
                elif eng.tab_jogo[letras.index(arg)][a] == '.':
                    matrix[letras.index(arg)][a] == 'O'
                    eng.settab_estado(matrix)
                else:
                    print('Perdeu!!! Fim do jogo!')
                    return True
            eng.print_tab_estado()
        else:
            print('Jogada inválida!')

    def do_coluna(self, arg):
        " - comando coluna que permite colocar o estado de todas as casas da coluna c que ainda não estão determinadas como sendo “água”...: coluna <c> \n"
        for a in range(len(eng.tab_estado)):
            eng.score += 1
            if eng.tab_estado[a][int(arg)-1] == 'X' or eng.tab_estado[a][int(arg)-1] == '*' or eng.tab_estado[a][int(arg)-1] == 'O': pass
            elif eng.tab_jogo[a][int(arg)-1] == '.':
                eng.tab_estado[a][int(arg)-1] == 'O'
            else:
                print('Perdeu!!! Fim do jogo!')
                return True
        else:
            print('Jogada inválida!')

    def do_ajuda(self, arg):
        " - comando ajuda que indica por linha e por coluna a quantidade de segmentos de barco existentes nessa linha/coluna..: ajuda  \n"
        pass
    
    def do_undo(self, arg):
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        eng.score -= 1
        pass
    
    def do_bot(self, arg):
        " - comando bot para apresentar a sequência de jogadas ótimas para terminar o jogo: bot \n"
        pass

    def do_gerar(self, arg):
        " - comando gerar que gera tabuleiros validos..: gerar \n"
        pass

    def do_score(self, arg):
        " - comando score que permite ver o registo ordenado dos scores dos jogadores..: \n"
        lst = list(self.dic)
        [[print(player, scor) for player in lst if self.dic[player] == scor] for scor in sorted(self.dic.values(), reverse=True)]

    def do_ver(self, arg):
        " - Comando para visualizar o estado atual do tabuleiro em ambiente grafico caso seja válido: VER  \n"
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        janela = BatalhaNavalWindow(40) 
        janela.mostraJanela(eng.gettab_estado())        
        
    def do_sair(self, arg):
        "Sair do programa BatalhaNaval: sair"
        print('Obrigado por ter utilizado o BatalhaNaval, espero que tenha sido divertido!')
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
                    del janela  # invoca o metodo destruidor de instancia __del__()
        return True


if __name__ == '__main__':
    eng = BatalhaNavalEngine()
    janela = None
    sh = BatalhaNavalShell()
    sh.cmdloop()
    
'''


'''

