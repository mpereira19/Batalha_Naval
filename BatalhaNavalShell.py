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
                eng.create_jogadas_history()
            else:
                print("Número de argumentos inválido!")
        except:
            print("Erro: ao mostrar o puzzle")

    def do_gravar(self, arg):
        " - comando gravar que leva como parâmetro o nome de um ficheiro e permite gravar o estado do jogo atual..: gravar <nome_ficheiro>  \n"
        import time
        try:
            matrix = eng.tab_jogo
            matrix1 = eng.tab_estado
            score = eng.score
            ficheiro = open(arg+'.txt', 'w')
            ficheiro.write('Tabuleiro:\n')

            for lines in range(len(matrix)):
                string = ''
                for col in range(len(matrix[lines])):
                    if col != len(matrix[lines])-1:
                        string += matrix[lines][col] + ' '
                    else:
                        string += matrix[lines][col] + '\n'
                ficheiro.write(string)
            ficheiro.write('Estado do Jogo:\n')

            for lines in range(len(matrix1)):
                string = ''
                for col in range(len(matrix1[lines])):
                    if col != len(matrix1[lines])-1:
                        string += matrix1[lines][col] + ' '
                    else:
                        string += matrix1[lines][col] + '\n'
                ficheiro.write(string)
            ficheiro.write('Jogadas efetuadas:\n')
            ficheiro.write(str(score))
            eng.score_files()
            estado = True
        except:
            print('Erro ao guardar o tabuleiro!')
            estado = False
        else:
            ficheiro.close()
            print('Jogo gravado com sucesso!!!')
        time.sleep(5)
        return estado
    
    def do_tiro(self, arg):
        '- comando tiro que leva como parâmetros a linha e a coluna de uma casa onde se pretende jogar..: tiro <l> <c>.\n'
        import time

        def ship_wreck_check(pos, mat_game, mat_cheat, confirmed_hits, saver):
            '''
            Esta função permite determinar a integridade de um navio. Isto é, se
        todas as posições 'barco' que lhe pertencem foram já ou não destruidas pelo jogador.
            
            Parameters
            ----------
            pos : Lst
                Posição onde o jogador acertou o tiro no barco.
            mat_game : Lst
                Matriz que representa o estado do jogo.
            mat_cheat : Lst
                Matriz com todas as posições "barco"
            confirmed_hits : Lst
                Lista com todas as posições que já foram ou não destruidas pelo jogador.
            Onde caso ainda não tenham sido destruidas é inserido uma string 'Alive'.
            saver : Lst
                Permite que o loop for final identifique posições ao redor de 
            todas as posições que constituem o barco

            Returns
            -------
            confirmed_hits : Lst
                Lista com todas as posições que constituem o barco onde o jogador acertou
            e se continua vivo ou não.

            '''
            
            
            for l in range(len(mat_cheat)):
                for c in range(len(mat_cheat[l])):
                    if [l, c] == [pos[0] - 1, pos[1] - 1] or [l, c] == [pos[0] - 1, pos[1]] or [l, c] == [pos[0] - 1, pos[1] + 1] or [l, c] == [pos[0], pos[1] - 1] or [l, c] == [pos[0], pos[1] + 1] or [l, c] == [pos[0] + 1, pos[1] - 1] or [l, c] == [pos[0] + 1, pos[1]] or [l, c] == [pos[0] + 1, pos[1]+1]:
                        if mat_game[l][c] == 'X' and mat_cheat[l][c] == '#' and ([l, c] not in confirmed_hits):
                            confirmed_hits.append([l, c])
                        elif mat_game[l][c] == '.' and mat_cheat[l][c] == '#' and ([l, c] not in confirmed_hits):
                            confirmed_hits.append('Alive')
                            confirmed_hits.append([l, c])
            if 'Alive' in confirmed_hits:
                return confirmed_hits
            else:
                if len(confirmed_hits) == 1:
                    return confirmed_hits
                else:
                    for i in confirmed_hits:
                        if i != 'Alive':
                            if i not in saver:
                                saver.append(i)
                                confirmed_hits = ship_wreck_check(i, mat_game, mat_cheat, confirmed_hits, saver)
                    return confirmed_hits
        try:
            l, c = arg.split()
            l = l.upper()
            if l in ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J'] and int(c) in [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]:
                c = int(c) - 1  # Localização da coluna posicional
                mat_cheat = eng.tab_jogo
                mat_jogador = eng.tab_estado
                for i, j in enumerate(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']):
                    if l == j:
                        l = int(i)  # Localização da linha posicional
                        break
                for lin in range(len(mat_jogador)):
                    for col in range(len(mat_jogador[lin])):
                        # identificação da ação da função do_tiro:
                        if mat_cheat[l][c] == '.' and [l, c] == [lin, col]:  # o tiro foi dado na água
                            mat_jogador[l][c] = 'O'
                            eng.settab_estado(mat_jogador)
                            eng.add_score()
                            eng.print_tab_estado()
                            print('\nAaaarrrrgggghhhh !!! Target missed...\n')
                            break
                        if mat_cheat[l][c] == '#' and [l, c] == [lin, col]:  # o tiro foi dado num barco
                            mat_jogador[l][c] = 'X'
                            eng.add_score()
                            eng.settab_estado(mat_jogador)
                            confirmed_hits = [[l, c]]
                            # função que permite saber a posição das restantes posições ocupadas pelo barco
                            lst_conf_hits = ship_wreck_check([l, c], mat_jogador, mat_cheat, confirmed_hits, saver=[])
                            if 'Alive' in lst_conf_hits:  # Se existirem mais posições ainda não descobertas avisa-se que o tiro acertou num barco sem o afundar
                                eng.print_tab_estado()
                                print("\nSHIVER ME TIMBERS !!! On the target but it won't go down...\n")
                            else:
                                for posi in lst_conf_hits:  # Caso contrário, se a str('Alive') não existir na lista de hits, todas as posições o barco foi destruido
                                    mat_jogador[posi[0]][posi[1]] = '*'
                                eng.settab_estado(mat_jogador)
                                eng.print_tab_estado()
                                print('\nSHIVER ME TIMBERS !!! Scuttle!! Target down!!\n')
                    count = sum([ lin.count('*') for lin in mat_jogador])
                    if count == 19:
                        print('\nSHIVER ME TIMBERS !!! Enemy down!! The war is won!!\n')
                        eng.score_files()
                        time.sleep(5)
                        return True
            else:
                print('Jogada inválida!')
        except:
            print('Jogada inválida!')

    def do_agua(self, arg):
        " - comando que leva como parâmetros a linha e a coluna de uma casa, pertencente a uma embarcação já afundada (totalmente descoberta) que se pretende rodear de “água”..: agua <l> <c> \n"
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        l, c = arg.split()
        c = int(c) - 1
        l = l.upper()
        for i, j in enumerate(letras):
            if j == l:
                l = int(i)
        loc = [l, c]
        mat = eng.tab_estado
        mat_c = eng.tab_jogo
        counter = []
        for a in range(len(mat)):
            for b in range(len(mat[a])):
                if [a, b] == [loc[0] - 1, loc[1] - 1] or [a, b] == [loc[0] - 1, loc[1]] or [a, b] == [loc[0] - 1, loc[1] + 1] or [a, b] == [loc[0], loc[1] - 1] or [a, b] == [loc[0], loc[1] + 1] or [a, b] == [loc[0] + 1, loc[1] - 1] or [a, b] == [loc[0] + 1, loc[1]] or [a, b] == [loc[0] + 1, loc[1] + 1]:
                    counter.append([a, b])
        counter.append(loc)

        for i in counter:
            if mat_c[i[0]][i[1]] == '#' and mat[i[0]][i[1]] == '.':
                print('\nAaaarrrrgggghhhh !!! Feed the fish! Fim do jogo!\n')
                return True

        for i in counter:
            if mat_c[i[0]][i[1]] == '.' and (mat[i[0]][i[1]] == '*' or mat[i[0]][i[1]] == 'O' or mat[i[0]][i[1]] == '.'):
                if mat[i[0]][i[1]] != '*':
                    mat[i[0]][i[1]] = 'O'
                    eng.settab_estado(mat)
        eng.print_tab_estado()
        print('\nAaaarrrrgggghhhh !!! Target missed... Only water!!\n')

    def do_linha(self, arg):
        " - comando linha que permite colocar o estado de todas as casas da linha l que ainda não estão determinadas como sendo “água”...: linha <l> \n"
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        import time
        try:
            arg = arg.upper()
            if arg in letras:
                eng.add_score()
                matrix = eng.tab_estado
                for a in range(len(matrix)):
                    if matrix[letras.index(arg)][a] == 'X' or matrix[letras.index(arg)][a] == '*' or matrix[letras.index(arg)][a] == 'O':
                        pass
                    elif eng.tab_jogo[letras.index(arg)][a] == '.':
                        matrix[letras.index(arg)][a] = 'O'
                    else:
                        print('\nAaaarrrrgggghhhh !!! Feed the fish! Fim do jogo!\n')
                        time.sleep(5)
                        return True
                eng.settab_estado(matrix)
                eng.print_tab_estado()
                eng.add_move()
                print('\nAaaarrrrgggghhhh !!! Target missed... Only water!!\n')
        except:
            print('Jogada inválida!')

    def do_coluna(self, arg):
        " - comando coluna que permite colocar o estado de tsheodas as casas da coluna c que ainda não estão determinadas como sendo “água”...: coluna <c> \n"
        numbers = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        import time
        if arg in numbers:
            eng.add_score()
            for a in range(len(eng.tab_estado)):
                matrix = eng.tab_estado
                if matrix[a][int(arg)-1] == 'X' or matrix[a][int(arg)-1] == '*' or matrix[a][int(arg)-1] == 'O':
                    pass
                elif eng.tab_jogo[a][int(arg)-1] == '.':
                    matrix[a][int(arg)-1] = 'O'
                else:
                    print('\nAAaaarrrrgggghhhh !!! Feed the fish! Fim do jogo!\n')
                    time.sleep(5)
                    return True
            eng.settab_estado(matrix)
            eng.print_tab_estado()
            eng.add_move()
            print('\nAaaarrrrgggghhhh !!! Target missed... Only water!!\n')
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
        print("[%s] Jogadas efetuadas:%d" % (eng.jogador, eng.get_score()))

    def do_undo(self, arg):
        " - comando para anular movimentos (retroceder no jogo): undo \n"
        eng.add_score()
        eng.undo_move()
        eng.print_tab_estado()
    
    def do_bot(self, arg):
        " - comando bot para apresentar a sequência de jogadas ótimas para terminar o jogo: bot \n"
        import time
        mat_c = eng.tab_jogo
        mat = eng.tab_estado
        lst_aimbot = []
        for i in range(len(mat)):
            for j in range(len(mat[i])):
                if mat_c[i][j] == '#' and mat[i][j] == '.':
                    lst_aimbot.append([i, j])
        target = lst_aimbot[-1]
        letras = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        target[0] = letras[target[0]]
        target[1] += 1
        self.do_tiro(target[0] + ' ' + str(target[1]))
        time.sleep(1)
        if len(lst_aimbot) != 1:
            self.do_bot('')
        return True

    def do_gerar(self, arg):
        " - comando gerar que gera tabuleiros validos..: gerar \n"
        import random

        def pos_checker2(checker, pos):
            '''

            Parameters
            ----------
            checker : TYPE
                A variavel 'checker' server para determinar se a variavel 'pos' é válida no contexto da matriz que representa o tabuleiro
            pos : TYPE
                Variavel que determina uma determinada posição válida(ou não) na matriz que representa o tabuleiro

            Returns
            -------
            check : TYPE
                True = Posição válida
                False = Posição fora dos limites da matriz

            '''
            if (10 not in pos) and (-1 not in pos):
                if pos not in checker:
                    check = True
                else:
                    check = False
            else:
                check = False
            return check

        def id_square(pos, checker, mat, pos_checker2):
            '''
            Função que identifica e guarda todas as 8 posições que rodeiam uma determinada posição

            Parameters
            ----------
            pos : Lst
                posição a procurar os identificadores que a rodeiam
            checker : Lst
                Checker é a lista que contem todas a posições válidas que rodeiam a "pos"
            mat : Lst
                Matriz identificadora do tabuleiro do jogo
            pos_checker2 : Func
                Função de determinação de posições válidas

            Returns
            -------
            checker : TYPE
                Lista com posições ( [linha,coluna] ) válidas que rodeiam a posição "pos"

            '''
            for l in range(len(mat)):
                for c in range(len(mat[l])):
                    if [l, c] == [pos[0] - 1, pos[1] - 1] or [l, c] == [pos[0] - 1, pos[1]] or [l, c] == [pos[0] - 1, pos[1] + 1] or [l, c] == [pos[0], pos[1] - 1] or [l, c] == [pos[0], pos[1] + 1] or [l, c] == [pos[0] + 1, pos[1] - 1] or [l, c] == [pos[0] + 1, pos[1]] or [l, c] == [pos[0] + 1, pos[1] + 1]:
                        if pos_checker2(checker, [l, c]) is True:
                            checker.append([l, c])
            return checker

        def pos_maker():
            '''
            Com recurso ao package Random, é possivel aleatóriamente criar posições, válidas, para serem marcadas como posição de um navio (ou parte do mesmo)
            
            Returns
            -------
            posicao : Lst
                posição aleatória onde é representada por um lista: [linha, coluna]

            '''
            posl = random.randint(0, 9)
            posc = random.randint(0, 9)
            posicao = [posl, posc]
            return posicao

        def make_turn(turn, pos):
            '''
            Como alguns navios têm mais de que 1 posição que lhes é atribuida, é necessário perceber qual é o lado que vão tomar. 
        
            Parameters
            ----------
            turn : string
                'R'-> Right | 'L'-> Left | 'U'-> Up | 'D'-> Down
                
            pos : Lst
                Posição inicial.

            Returns
            -------
            pos_turn : Lst
                Posição seguinte e o lado que lhe é atribuida.

            '''
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
            '''
            O navio Cruzador é constituido por 4 casas seguidas e como não possiu uma
        posição central, assomiu-se que esta seria a posição 2 que lhe diz respeito.
        A posição do barco será gerada bem como o lado de viragem

            Parameters
            ----------
            turn : string
                'R'-> Right | 'L'-> Left | 'U'-> Up | 'D'-> Down
            pos : Lst
                Posição central do cruzador
            checker : Lst
                A lista checker é uma lista com todas as posições ocupadas por navios.
            Serve de confirmação para posições que ainda não foram acupadas por outros navios.

            Returns
            -------
            TYPE
                False-> Se alguma possivel posição é inválida (fora dos limites da matriz ou já ocupada)
                
                Caso todas as posições sejam válidas, dá return a uma lista com as mesmas.

            '''
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
            '''
            O porta-aviões é um navio que ocupa 5 casas: 3 por 2 (forma T).
            É necessário gerar 5 posições em forma de T que sejam válidas.
            A posição central do porta aviões é a posição que liga a parte vertical
        à horizontal.

            Parameters
            ----------
            turn : string
                'R'-> Right | 'L'-> Left | 'U'-> Up | 'D'-> Down
            pos : TYPE
                Posição central do porta-aviões
            checker : TYPE
                Lista com as posições já ocupadas por barcos.

            Returns
            -------
            TYPE
                False -> se alguma das posições é inválida ou já ocupada.
                
                Caso todas as posições sejam válidas dá return a uma lista com as mesmas

            '''
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
        import os
        try:
            if os.path.exists('Score.txt') is False:
                print('No score data!!!')

            elif os.path.exists('Score.txt') is True:
                file = open('Score.txt', 'r')
                data = file.readlines()[1:]
                file.close()
                data1 = [line.replace('\n', '').split() for line in data]
                dic = {line[0]: int(line[1]) for line in data1}
                key = list(dic)
                values = sorted(dic.values(), reverse=True)
                print('Scores:')
                for val in values:
                    for k in key:
                        if dic[k] == val:
                            print(f'{values.index(val)+1}º. {k}  {val}')
        except:
            print('Erro!!!')

    def do_ver(self, arg):
        " - Comando para visualizar o estado atual do tabuleiro em ambiente grafico caso seja válido: VER  \n"
        global janela  # pois pretendo atribuir um valor a um identificador global
        if janela is not None:
            del janela  # invoca o metodo destruidor de instancia __del__()
        janela = BatalhaNavalWindow(40) 
        janela.mostraJanela(eng.gettab_estado())        
        
    def do_sair(self, arg):
        "Sair do programa BatalhaNaval: sair"
        eng.score_files()
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

