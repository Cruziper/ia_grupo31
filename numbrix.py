# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 31:
# 84721 Gonçalo Cruz
# 98789 António Cunha

import copy
import sys

from search import Problem, Node, astar_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search

###################################################################################################
#                                         NUMBRIXSTATE                                            #
###################################################################################################
class NumbrixState:
    state_id = 0

    def __init__(self, board):
        self.board = board
        self.id = NumbrixState.state_id
        NumbrixState.state_id += 1

    def __lt__(self, other):
        return self.id < other.id
        
    # TODO: outros metodos da classe


###################################################################################################
#                                             BOARD                                               #
###################################################################################################
class Board:
    boardSize = 0
    board = []
    """ Representação interna de um tabuleiro de Numbrix. """
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self.board[self.findRow(row)][self.findColumn(col)]
    
    def adjacent_vertical_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if (row-1 >= 1):
            if(row+1 <= self.boardSize):
                """ Se tiver casa imediatamente abaixo e acima
                Return: ([linha+1][coluna], [linha-1][coluna]) """
                return (int(self.get_number(row+1, col)), int(self.get_number(row-1, col)))
            else:
                """ Se tiver apenas casa imediatamente acima
                Return: (None, [linha-1][coluna]) """
                return (None, int(self.get_number(row-1, col)))
        else:
            if(row+1 <= self.boardSize):
                """ Se tiver apenas casa imediatamente abaixo
                Return: ([linha+1][coluna], None) """
                return (int(self.get_number(row+1, col)), None)
    
    def adjacent_horizontal_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        if (col-1 >= 1):
            if(col+1 <= self.boardSize):
                """ Se tiver casa imediatamente à esquerda e à direita
                Return: ([linha][coluna-1], [linha][coluna+1]) """
                return (int(self.get_number(row, col-1)), int(self.get_number(row, col+1)))
            else:
                """ Se tiver apenas casa imediatamente à esquerda
                Return: ([linha][coluna-1], None) """
                return (int(self.get_number(row, col-1)), None)
        else:
            if(col <= self.boardSize):
                """ Se tiver apenas casa imediatamente à direita
                Return: (None, [linha][coluna+1]) """
                return (None, int(self.get_number(row, col+1)))
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        boardClass = Board()
        board = []
        with open(filename, "r") as f:
            # index 0 --> N
            boardClass.boardSize = int(f.readline())
            for line in f:
                row = [int(column.strip()) for column in line.split('\t')]
                board.append(row)
        boardClass.board = board
        return boardClass

    def findRow(self, row: int):
        """ devolve o valor do index da linha """
        return row-1
    
    def findColumn(self, col: int):
        """ devolve o valor do index da coluna """
        return col-1

    def __size__():
        return Board.boardSize

    def initializeBoard (self, boardL: list):
        self.board = copy.deepcopy(boardL)
        self.boardSize = len(boardL)
        


###################################################################################################
#                                            NUMBRIX                                              #
###################################################################################################
class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        return NumbrixState.__init__(self, board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. 
        RETURN: [(linha, coluna, valor),(linha, coluna, valor),(linha, coluna, valor), ...]"""
        board = state.board.board
        print("\nBoard:")
        print(board)
        not_unique = True
        possible_neighbors = []
        actions = []

        for i in range (len(board)):
            for j in range (len(board)):
                possible_neighbors = []
                if int(board[i][j]) == 0:
                    not_unique = True
                    horiz_nei = list(state.board.adjacent_horizontal_numbers(i+1, j+1))
                    vert_nei = list(state.board.adjacent_vertical_numbers(i+1, j+1))
                    if horiz_nei[0] != None and horiz_nei[1] != None:
                        if horiz_nei[1] == horiz_nei[0]+2:
                            possible_neighbors.append(horiz_nei[0]+1)
                            not_unique = False
                        if horiz_nei[1] == horiz_nei[0]-2:
                            possible_neighbors.append(horiz_nei[0]-1)
                            not_unique = False
                    if vert_nei[0] != None and vert_nei[1] != None:
                        if vert_nei[1] == vert_nei[0]+2:
                            possible_neighbors.append(vert_nei[0]+1)
                            not_unique = False
                        if vert_nei[1] == vert_nei[0]-2:
                            possible_neighbors.append(vert_nei[0]-1)
                            not_unique = False

                    ######################################################## ESQUERDA ########################################################
                    if horiz_nei[0] != None and not_unique:
                        # se for possivel seguir pela esquerda
                        ## MAIS UM ##
                        if int(horiz_nei[0])+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if int(horiz_nei[0])+1 not in possible_neighbors:
                                possible_neighbors.append(horiz_nei[0]+1)
                        else:
                            if (int(horiz_nei[0]+1) < len(board)*len(board)):
                                # caso não seja devo verificar se terá continuação possivel
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if int(horiz_nei[1]) == 0 or int(horiz_nei[1]) == int(horiz_nei[0])+2:
                                        if int(horiz_nei[0])+1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[0]+1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if int(vert_nei[0]) == 0 or int(vert_nei[0]) == int(horiz_nei[0])+2:
                                        if int(horiz_nei[0])+1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[0]+1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if int(vert_nei[1]) == 0 or int(vert_nei[1]) == int(horiz_nei[0])+2:
                                        if int(horiz_nei[0])+1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[0]+1)
                        ## MENOS UM ##
                        if int(horiz_nei[0])-1 == 1:
                            # se o valor a colocar for o primeiro
                            if int(horiz_nei[0])-1 not in possible_neighbors:
                                possible_neighbors.append(horiz_nei[0]-1)
                        else:
                            if int(horiz_nei[0])-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if int(horiz_nei[1]) == 0 or int(horiz_nei[1]) == int(horiz_nei[0])-2:
                                        if int(horiz_nei[0])-1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[0]-1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if int(vert_nei[0]) == 0 or int(vert_nei[0]) == int(horiz_nei[0])-2:
                                        if int(horiz_nei[0])-1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[0]-1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if int(vert_nei[1]) == 0 or int(vert_nei[1]) == int(horiz_nei[0])-2:
                                        if int(horiz_nei[0])-1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[0]-1)
                    ##########################################################################################################################

                    ######################################################## DIREITA #########################################################
                    if horiz_nei[1] != None and not_unique:
                        # se for possivel seguir pela direita
                        ## MAIS UM ##
                        if int(horiz_nei[1])+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if int(horiz_nei[1])+1 not in possible_neighbors:
                                possible_neighbors.append(horiz_nei[1]+1)
                        else:
                            if int(horiz_nei[1])+1 < len(board)*len(board):
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if int(horiz_nei[0]) == 0 or int(horiz_nei[0]) == int(horiz_nei[1])+2:
                                        if int(horiz_nei[1])+1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[1]+1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if int(vert_nei[0]) == 0 or int(vert_nei[0]) == int(horiz_nei[1])+2:
                                        if int(horiz_nei[1])+1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[1]+1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if int(vert_nei[1]) == 0 or int(vert_nei[1]) == int(horiz_nei[1])+2:
                                        if int(horiz_nei[1])+1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[1]+1)
                        ## MENOS UM ##
                        if int(horiz_nei[1])-1 == 1:
                            # se o valor a colocar for o primeiro
                            if int(horiz_nei[1])-1 not in possible_neighbors:
                                possible_neighbors.append(horiz_nei[1]-1)
                        else:
                            if int(horiz_nei[1])-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if int(horiz_nei[0]) == 0 or int(horiz_nei[0]) == int(horiz_nei[1])-2:
                                        if int(horiz_nei[1])-1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[1]-1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if int(vert_nei[0]) == 0 or int(vert_nei[0]) == int(horiz_nei[1])-2:
                                        if int(horiz_nei[1])-1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[1]-1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if int(vert_nei[1]) == 0 or int(vert_nei[1]) == int(horiz_nei[1])-2:
                                        if int(horiz_nei[1])-1 not in possible_neighbors:
                                            possible_neighbors.append(horiz_nei[1]-1)
                    ##########################################################################################################################

                    ######################################################### BAIXO ##########################################################
                    if vert_nei[0] != None and not_unique:
                        # se for possivel seguir para baixo
                        ## MAIS UM ##
                        if int(vert_nei[0])+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if int(vert_nei[0])+1 not in possible_neighbors:
                                possible_neighbors.append(vert_nei[0]+1)
                        else:
                            if int(vert_nei[0])+1 < len(board)*len(board):
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if int(horiz_nei[0]) == 0 or int(horiz_nei[0]) == int(vert_nei[0])+2:
                                        if int(vert_nei[0])+1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[0]+1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if int(horiz_nei[1]) == 0 or int(horiz_nei[1]) == int(vert_nei[0])+2:
                                        if int(vert_nei[0])+1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[0]+1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if int(vert_nei[1]) == 0 or int(vert_nei[1]) == int(vert_nei[0])+2:
                                        if int(vert_nei[0])+1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[0]+1)
                        ## MENOS UM ##
                        if int(vert_nei[0])-1 == 1:
                            # se o valor a colocar for o primeiro
                            if int(vert_nei[0])-1 not in possible_neighbors:
                                possible_neighbors.append(vert_nei[0]-1)
                        else:
                            if int(vert_nei[0])-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if int(horiz_nei[0]) == 0 or int(horiz_nei[0]) == int(vert_nei[0])-2:
                                        if int(vert_nei[0])-1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[0]-1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if int(horiz_nei[1]) == 0 or int(horiz_nei[1]) == int(vert_nei[0])-2:
                                        if int(vert_nei[0])-1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[0]-1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if int(vert_nei[1]) == 0 or int(vert_nei[1]) == int(vert_nei[0])-2:
                                        if int(vert_nei[0])-1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[0]-1)
                    ##########################################################################################################################

                    ########################################################## CIMA ##########################################################
                    if vert_nei[1] != None and not_unique:
                        # se for possivel seguir para baixo
                        ## MAIS UM ##
                        if int(vert_nei[1])+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if int(vert_nei[1])+1 not in possible_neighbors:
                                possible_neighbors.append(vert_nei[1]+1)
                        else:
                            if int(vert_nei[1])+1 < len(board)*len(board):
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if int(horiz_nei[0]) == 0 or int(horiz_nei[0]) == int(vert_nei[1])+2:
                                        if int(vert_nei[1])+1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[1]+1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if int(horiz_nei[1]) == 0 or int(horiz_nei[1]) == int(vert_nei[1])+2:
                                        if int(vert_nei[1])+1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[1]+1)
                                    
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if int(vert_nei[0]) == 0 or int(vert_nei[0]) == int(vert_nei[1])+2:
                                        if int(vert_nei[1])+1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[1]+1)
                        ## MENOS UM ##
                        if int(vert_nei[1])-1 == 1:
                            # se o valor a colocar for o primeiro
                            if int(vert_nei[1])-1 not in possible_neighbors:
                                possible_neighbors.append(vert_nei[1]-1)
                        else:
                            if int(vert_nei[1])-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if int(horiz_nei[0]) == 0 or int(horiz_nei[0]) == int(vert_nei[1])-2:
                                        if int(vert_nei[1])-1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[1]-1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if int(horiz_nei[1]) == 0 or int(horiz_nei[1]) == int(vert_nei[1])-2:
                                        if int(vert_nei[1])-1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[1]-1)
                                    
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if int(vert_nei[0]) == 0 or int(vert_nei[0]) == int(vert_nei[1])-2:
                                        if int(vert_nei[1])-1 not in possible_neighbors:
                                            possible_neighbors.append(vert_nei[1]-1)
                    ##########################################################################################################################

                    possible_actions = Numbrix.optimize_actions(self, board, possible_neighbors)
                    for x in possible_actions:
                        actions.append((i+1,j+1,x))
        print("\nActions:")
        print(actions)
        return actions

    def select_next_action(self, actions, size):
        selected_action = ()
        # conta o número de ações para determinado valor
        freq = [0] * size
        for action in actions:
            freq[action[2]-1]+=1
        
        for i in range (len(freq)):
            if freq[i] != 0:
                current_min = freq[i]
                break;
        
        # retorna o index da action do valor com menos frequência
        for i in range (len(freq)):
            if freq[i] != 0 and freq[i] <= current_min:
                index = i

        for action in actions:
            if action[2] == index+1:
                selected_action = action

        return selected_action


    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        boardAux = Board()
        boardAux.initializeBoard(state.board.board)
        new_state = NumbrixState(boardAux)
        if action != ():
            row = action[0]
            col = action[1]
            nmbr = action[2]
            print(new_state.board)
            new_state.board.board[row-1][col-1] = nmbr
        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        for i in range (len(state.board)):
            for j in range (len(state.board)):
                if int(state.board[i][j]) == 0:
                    return False
        return True


    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    def optimize_actions(self, board: Board, actions: list):
        
        for i in range (len(board)):
            for j in range (len(board)):
                if int(board[i][j]) in actions:
                    actions.remove(int(board[i][j]))
        
        return actions


###################################################################################################
#                                             MAIN                                                #
###################################################################################################
if __name__ == "__main__":

    # Ler o ficheiro de input de sys.argv[1],
    board = Board.parse_instance(sys.argv[1])
    problem = Numbrix(board.board)
    initial_state = NumbrixState(board)
    result_state = problem.result(initial_state, (1, 2, 2))
    print(initial_state.board.board)

    print(result_state.board.board)
    print(result_state.board.get_number(2, 2))
    actions = Numbrix.actions(problem, result_state)
    
    # Usar uma técnica de procura para resolver a instância,

    # Retirar a solução a partir do nó resultante,

    # Imprimir para o standard output no formato indicado.
    pass
