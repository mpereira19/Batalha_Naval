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

    players_score = {}

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
                ficheiro.write(*eng.tab_jogo[lines])
            ficheiro.writelines('Estado do Jogo:')
            for lines in range(len(eng.tab_estado)):
                ficheiro.write(*eng.tab_estado[lines])
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
        import time
        if arg in letras:
            eng.score += 1
            matrix = eng.tab_estado
            for a in range(len(matrix)):
                if matrix[letras.index(arg)][a] == 'X' or matrix[letras.index(arg)][a] == '*' or matrix[letras.index(arg)][a] == 'O':
                    pass
                elif eng.tab_jogo[letras.index(arg)][a] == '.':
                    matrix[letras.index(arg)][a] = 'O'
                else:
                    print('Perdeu!!! Fim do jogo!')
                    time.sleep(5)
                    return True
            eng.settab_estado(matrix)
            eng.print_tab_estado()
        else:
            print('Jogada inválida!')

    def do_coluna(self, arg):
        " - comando coluna que permite colocar o estado de tsheodas as casas da coluna c que ainda não estão determinadas como sendo “água”...: coluna <c> \n"
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        import time
        if arg in numbers:
            eng.score += 1
            for a in range(len(eng.tab_estado)):
                matrix = eng.tab_estado
                if matrix[a][int(arg)-1] == 'X' or matrix[a][int(arg)-1] == '*' or matrix[a][int(arg)-1] == 'O':
                    pass
                elif eng.tab_jogo[a][int(arg)-1] == '.':
                    matrix[a][int(arg)-1] = 'O'
                else:
                    print('Perdeu!!! Fim do jogo!')
                    time.sleep(5)
                    return True
            eng.settab_estado(matrix)
        else:
            print('Jogada inválida!')

    def do_ajuda(self, arg):
        " - comando ajuda que indica por linha e por coluna a quantidade de segmentos de barco existentes nessa linha/coluna..: ajuda  \n"
        count_line = []
        count_column = '\n   '
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        for line in range(len(eng.tab_jogo)):
            count_line.append(eng.tab_jogo[line].count('#'))
            transposta = [[eng.tab_jogo[col][line] for col in range(len(eng.tab_jogo[line]))] for line in range(len(eng.tab_jogo))]
            count_column += ' ' + str(transposta[line].count('#'))
        print(count_column)
        print("    1 2 3 4 5 6 7 8 9 10")
        i = 0
        for linha in eng.tab_estado:
            print(f'{count_line[i]}>{letras[i]}', end=' ')
            i += 1
            for simbolo in linha:
                print(simbolo, end=" ")
            print()
        print("[%s] Jogadas efetuadas:%d" % (eng.jogador, eng.score))

    
    def do_undo(self, arg):
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        eng.score += 1
        pass
    
    def do_bot(self, arg):
        " - comando bot para apresentar a sequência de jogadas ótimas para terminar o jogo: bot \n"
        pass

    def do_gerar(self, arg):
        " - comando gerar que gera tabuleiros validos..: gerar \n"
        import random

        def pos_checker2(checker, pos):
            if (10 not in pos) and (-1 not in pos):
                if pos not in checker:
                    check = True
                else:
                    check = False
            else:
                check = False
            return check

        def id_square(pos, checker, mat, pos_checker2):
            for l in range(len(mat)):
                for c in range(len(mat[l])):
                    if [l, c] == [pos[0] - 1, pos[1] - 1] or [l, c] == [pos[0] - 1, pos[1]] or [l, c] == [pos[0] - 1, pos[1] + 1] or [l, c] == [pos[0], pos[1] - 1] or [l, c] == [pos[0], pos[1] + 1] or [l, c] == [pos[0] + 1, pos[1] - 1] or [l, c] == [pos[0] + 1, pos[1]] or [l, c] == [pos[0] + 1, pos[1] + 1]:
                        if pos_checker2(checker, [l, c]) is True:
                            checker.append([l, c])
            return checker

        def pos_maker():
            posl = random.randint(0, 9)
            posc = random.randint(0, 9)
            posicao = [posl, posc]
            return posicao

        def make_turn(turn, pos):
            if turn == 'U':
                pos_turn = [pos[0] - 1, pos[1]]
            if turn == 'D':
                pos_turn = [pos[0] + 1, pos[1]]
            if turn == 'R':
                pos_turn = [pos[0], pos[1] + 1]
            if turn == 'L':
                pos_turn = [pos[0], pos[1] - 1]
            return pos_turn

        def cruzador(turn, pos, checker):
            if turn == 'R':
                turn1 = make_turn('R', pos)
                turn2 = make_turn('R', turn1)
                turn3 = make_turn('L', pos)
                lst_pos_crz = [turn1, turn2, turn3]
                for i in lst_pos_crz:
                    if pos_checker2(checker, i) is False:
                        return False
            if turn == 'L':
                turn1 = make_turn('L', pos)
                turn2 = make_turn('L', turn1)
                turn3 = make_turn('R', pos)
                lst_pos_crz = [turn1, turn2, turn3]
                for i in lst_pos_crz:
                    if pos_checker2(checker, i) is False:
                        return False
            if turn == 'U':
                turn1 = make_turn('U', pos)
                turn2 = make_turn('U', turn1)
                turn3 = make_turn('D', pos)
                lst_pos_crz = [turn1, turn2, turn3]
                for i in lst_pos_crz:
                    if pos_checker2(checker, i) is False:
                        return False
            if turn == 'D':
                turn1 = make_turn('D', pos)
                turn2 = make_turn('D', turn1)
                turn3 = make_turn('U', pos)
                lst_pos_crz = [turn1, turn2, turn3]
                for i in lst_pos_crz:
                    if pos_checker2(checker, i) is False:
                        return False
            return lst_pos_crz

        def porta_avioes(turn, pos, checker):
            if turn == 'R':
                turn1 = make_turn('U', pos)
                turn2 = make_turn('D', pos)
                turn3 = make_turn('R', pos)
                turn4 = make_turn('R', turn3)
                lst_pos_av = [turn1, turn2, turn3, turn4]
                for i in lst_pos_av:
                    if pos_checker2(checker, i) is False:
                        return False
            if turn == 'L':
                turn1 = make_turn('U', pos)
                turn2 = make_turn('D', pos)
                turn3 = make_turn('L', pos)
                turn4 = make_turn('L', turn3)
                lst_pos_av = [turn1, turn2, turn3, turn4]
                for i in lst_pos_av:
                    if pos_checker2(checker, i) is False:
                        return False
            if turn == 'U':
                turn1 = make_turn('R', pos)
                turn2 = make_turn('L', pos)
                turn3 = make_turn('U', pos)
                turn4 = make_turn('U', turn3)
                lst_pos_av = [turn1, turn2, turn3, turn4]
                for i in lst_pos_av:
                    if pos_checker2(checker, i) is False:
                        return False
            if turn == 'D':
                turn1 = make_turn('R', pos)
                turn2 = make_turn('L', pos)
                turn3 = make_turn('D', pos)
                turn4 = make_turn('D', turn3)
                lst_pos_av = [turn1, turn2, turn3, turn4]
                for i in lst_pos_av:
                    if pos_checker2(checker, i) is False:
                        return False
            return lst_pos_av

        mat_pos = []
        for l in range(10):
            lst_dot = []
            for c in range(10):
                lst_dot.append('.')
            mat_pos.append(lst_dot)

        checker = []  # Guarda as posicoes de cada '#' correspondente a um navio

        n_submarinos = 0
        while n_submarinos < 3:
            pos = pos_maker()
            if pos_checker2(checker, pos) is True:
                checker.append(pos)
                checker = id_square(pos, checker, mat_pos, pos_checker2)
                mat_pos[pos[0]][pos[1]] = 's'
                n_submarinos += 1

        n_rebocadores = 0
        while n_rebocadores < 2:
            pos_barco = pos_maker()
            if pos_checker2(checker, pos_barco) is True:
                turn = random.choice(['U', 'D', 'L', 'R'])
                pos_turn = make_turn(turn, pos_barco)
                if pos_checker2(checker, pos_turn) is True:
                    checker.append(pos_barco)
                    checker.append(pos_turn)
                    checker = id_square(pos_barco, checker, mat_pos, pos_checker2)
                    checker = id_square(pos_turn, checker, mat_pos, pos_checker2)
                    mat_pos[pos_barco[0]][pos_barco[1]] = 'r'
                    mat_pos[pos_turn[0]][pos_turn[1]] = 'r'
                    n_rebocadores += 1

        n_contratorpedeiro = 0
        while n_contratorpedeiro < 1:
            pos_cp = pos_maker()
            if pos_checker2(checker, pos_cp) is True:
                turn = random.choice(['U', 'R'])
                if turn == 'R':
                    pos_turn1 = make_turn('R', pos_cp)
                    pos_turn2 = make_turn('L', pos_cp)
                    if (pos_checker2(checker, pos_turn1) is True) and (pos_checker2(checker, pos_turn2) is True):
                        checker.append(pos_cp)
                        checker.append(pos_turn1)
                        checker.append(pos_turn2)
                        checker = id_square(pos_cp, checker, mat_pos, pos_checker2)
                        checker = id_square(pos_turn1, checker, mat_pos, pos_checker2)
                        checker = id_square(pos_turn2, checker, mat_pos, pos_checker2)
                        mat_pos[pos_cp[0]][pos_cp[1]] = 'c'
                        mat_pos[pos_turn1[0]][pos_turn1[1]] = 'c'
                        mat_pos[pos_turn2[0]][pos_turn2[1]] = 'c'
                        n_contratorpedeiro += 1
                else:
                    pos_turn1 = make_turn('U', pos_cp)
                    pos_turn2 = make_turn('D', pos_cp)
                    if (pos_checker2(checker, pos_turn1) is True) and (pos_checker2(checker, pos_turn2) is True):
                        checker.append(pos_cp)
                        checker.append(pos_turn1)
                        checker.append(pos_turn2)
                        checker = id_square(pos_cp, checker, mat_pos, pos_checker2)
                        checker = id_square(pos_turn1, checker, mat_pos, pos_checker2)
                        checker = id_square(pos_turn2, checker, mat_pos, pos_checker2)
                        mat_pos[pos_cp[0]][pos_cp[1]] = 'c'
                        mat_pos[pos_turn1[0]][pos_turn1[1]] = 'c'
                        mat_pos[pos_turn2[0]][pos_turn2[1]] = 'c'
                        n_contratorpedeiro += 1

        n_cruzador = 0
        while n_cruzador < 1:
            pos_crz = pos_maker()
            if pos_checker2(checker, pos_crz) is True:
                turn = random.choice(['U', 'D', 'L', 'R'])
                lst_crz = cruzador(turn, pos_crz, checker)
                if lst_crz is not False:
                    mat_pos[pos_crz[0]][pos_crz[1]] = 'X'
                    checker.append(pos_crz)
                    for pos_resto_crz in lst_crz:
                        mat_pos[pos_resto_crz[0]][pos_resto_crz[1]] = 'X'
                        checker.append(pos_resto_crz)
                        checker = id_square(pos_crz, checker, mat_pos, pos_checker2)
                        checker = id_square(pos_resto_crz, checker, mat_pos, pos_checker2)
                        n_cruzador += 1

        n_porta_avioes = 0
        while n_porta_avioes < 1:
            pos_pa = pos_maker()
            if pos_checker2(checker, pos_pa) is True:
                turn = random.choice(['U', 'D', 'L', 'R'])
                lst_pa = porta_avioes(turn, pos_pa, checker)
                if lst_pa is not False:
                    mat_pos[pos_pa[0]][pos_pa[1]] = 'A'
                    checker.append(pos_pa)
                    for pos_porta_av in lst_pa:
                        mat_pos[pos_porta_av[0]][pos_porta_av[1]] = 'A'
                        checker.append(pos_porta_av)
                        checker = id_square(pos_pa, checker, mat_pos, pos_checker2)
                        checker = id_square(pos_porta_av, checker, mat_pos, pos_checker2)
                        n_porta_avioes += 1

        estado = []
        for l in range(10):
            lst_dot = []
            for c in range(10):
                lst_dot.append('.')
            estado.append(lst_dot)

        for line in range(len(mat_pos)):
            for col in range(len(mat_pos[line])):
                if mat_pos[line][col] != '.':
                    mat_pos[line][col] = '#'
        try:
            file = open(arg, 'w')
            file.write('Tabuleiro:\n')

            for l in range(len(mat_pos)):
                for c in range(len(mat_pos[l])):
                    if c != len(mat_pos[l]) - 1:
                        file.write(mat_pos[l][c] + ' ')
                    else:
                        file.write(mat_pos[l][c])
                file.writelines('\n')
            file.write('Estado do Jogo:\n')

            for l2 in range(len(estado)):
                for c2 in range(len(estado[l2])):
                    if c2 != len(estado[l2]) - 1:
                        file.write(estado[l2][c2] + ' ')
                    else:
                        file.write(estado[l2][c2])
                file.writelines('\n')

            file.write('Jogadas efetuadas:\n0')
        finally:
            file.close()


    def do_score(self, arg):
        " - comando score que permite ver o registo ordenado dos scores dos jogadores..: \n"
        pass

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

