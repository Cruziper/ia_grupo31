# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 31:
# 84721 Gonçalo Cruz
# 98789 António Cunha

import copy
import sys

from search import Problem, Node, astar_search, breadth_first_graph_search, breadth_first_tree_search, depth_first_tree_search, greedy_search, recursive_best_first_search
from utils import manhattan_distance

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

###################################################################################################
#                                             BOARD                                               #
###################################################################################################
class Board:
    boardSize = 0
    board = []
    board_nums = []
    board_cells = []
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
        i = 0
        with open(filename, "r") as f:
            # index 0 --> N
            boardClass.boardSize = int(f.readline())
            for line in f:
                row = [int(column.strip()) for column in line.split('\t')]
                for j in range (len(row)):
                    if row[j] != 0:
                        boardClass.board_nums.append(row[j])
                        boardClass.board_cells.append((i+1, j+1, row[j]))
                i += 1
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

    def initializeBoard (self, boardL: list, nums: list, board_cells: list):
        self.board = copy.deepcopy(boardL)
        self.boardSize = len(boardL)
        self.board_nums = copy.deepcopy(nums)
        self.board_cells = copy.deepcopy(board_cells)
    
    def to_string(self):
        board_str=""
        for i in range (len(self.board)):
            for j in range (len(self.board)):
                board_str += str(self.board[i][j])
                if j < len(self.board)-1:
                    board_str += "\t"
            if i < len(self.board)-1:
                board_str += "\n"
        return board_str


###################################################################################################
#                                            NUMBRIX                                              #
###################################################################################################
class Numbrix(Problem):
    uni_actions = []

    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. 
        RETURN: [(linha, coluna, valor),(linha, coluna, valor),(linha, coluna, valor), ...]"""
        board = state.board.board
        # print("\nBoard:\n", state.board.to_string())
        actions = []

        for i in range (len(board)):
            for j in range (len(board)):
                possible_neighbors = []
                if board[i][j] == 0:
                    not_unique = True
                    horiz_nei = list(state.board.adjacent_horizontal_numbers(i+1, j+1))
                    vert_nei = list(state.board.adjacent_vertical_numbers(i+1, j+1))
                    if horiz_nei[0] != None and horiz_nei[1] != None and horiz_nei[0] != 0 and horiz_nei[1] != 0:
                        if horiz_nei[1] == horiz_nei[0]+2 and horiz_nei[0]+1 not in state.board.board_nums:
                            possible_neighbors.append(horiz_nei[0]+1)
                            not_unique = False
                        if horiz_nei[1] == horiz_nei[0]-2 and horiz_nei[0]-1 not in state.board.board_nums:
                            possible_neighbors.append(horiz_nei[0]-1)
                            not_unique = False
                    if vert_nei[0] != None and vert_nei[1] != None and vert_nei[0] != 0 and vert_nei[1] != 0:
                        if vert_nei[1] == vert_nei[0]+2 and vert_nei[0]+1 not in state.board.board_nums:
                            possible_neighbors.append(vert_nei[0]+1)
                            not_unique = False
                        if vert_nei[1] == vert_nei[0]-2 and vert_nei[0]-1 not in state.board.board_nums:
                            possible_neighbors.append(vert_nei[0]-1)
                            not_unique = False

                    ######################################################## ESQUERDA ########################################################
                    if horiz_nei[0] != None and not_unique:
                        # se for possivel seguir pela esquerda
                        ## MAIS UM ##
                        if horiz_nei[0]+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if horiz_nei[0]+1 not in possible_neighbors and horiz_nei[0]+1 not in state.board.board_nums:
                                possible_neighbors.append(horiz_nei[0]+1)
                        else:
                            if horiz_nei[0]+1 < len(board)*len(board) and horiz_nei[0]+1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if horiz_nei[1] == 0 or horiz_nei[1] == horiz_nei[0]+2:
                                        if horiz_nei[0]+1 not in possible_neighbors and horiz_nei[0]+1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[0]+1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if vert_nei[0] == 0 or vert_nei[0] == horiz_nei[0]+2:
                                        if horiz_nei[0]+1 not in possible_neighbors and horiz_nei[0]+1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[0]+1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if vert_nei[1] == 0 or vert_nei[1] == horiz_nei[0]+2:
                                        if horiz_nei[0]+1 not in possible_neighbors and horiz_nei[0]+1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[0]+1)
                        ## MENOS UM ##
                        if horiz_nei[0]-1 == 1:
                            # se o valor a colocar for o primeiro
                            if horiz_nei[0]-1 not in possible_neighbors and horiz_nei[0]-1 not in state.board.board_nums :
                                possible_neighbors.append(horiz_nei[0]-1)
                        else:
                            if horiz_nei[0]-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if horiz_nei[1] == 0 or horiz_nei[1] == horiz_nei[0]-2:
                                        if horiz_nei[0]-1 not in possible_neighbors and horiz_nei[0]-1 not in state.board.board_nums :
                                            possible_neighbors.append(horiz_nei[0]-1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if vert_nei[0] == 0 or vert_nei[0] == horiz_nei[0]-2:
                                        if horiz_nei[0]-1 not in possible_neighbors and horiz_nei[0]-1 not in state.board.board_nums :
                                            possible_neighbors.append(horiz_nei[0]-1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if vert_nei[1] == 0 or vert_nei[1] == horiz_nei[0]-2:
                                        if horiz_nei[0]-1 not in possible_neighbors and horiz_nei[0]-1 not in state.board.board_nums :
                                            possible_neighbors.append(horiz_nei[0]-1)
                    ##########################################################################################################################

                    ######################################################## DIREITA #########################################################
                    if horiz_nei[1] != None and not_unique:
                        # se for possivel seguir pela direita
                        ## MAIS UM ##
                        if horiz_nei[1]+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if horiz_nei[1]+1 not in possible_neighbors and horiz_nei[1]+1 not in state.board.board_nums:
                                possible_neighbors.append(horiz_nei[1]+1)
                        else:
                            if horiz_nei[1]+1 < len(board)*len(board) and horiz_nei[1]+1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if horiz_nei[0] == 0 or horiz_nei[0] == horiz_nei[1]+2:
                                        if horiz_nei[1]+1 not in possible_neighbors and horiz_nei[1]+1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[1]+1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if vert_nei[0] == 0 or vert_nei[0] == horiz_nei[1]+2:
                                        if horiz_nei[1]+1 not in possible_neighbors and horiz_nei[1]+1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[1]+1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if vert_nei[1] == 0 or vert_nei[1] == horiz_nei[1]+2:
                                        if horiz_nei[1]+1 not in possible_neighbors and horiz_nei[1]+1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[1]+1)
                        ## MENOS UM ##
                        if horiz_nei[1]-1 == 1:
                            # se o valor a colocar for o primeiro
                            if horiz_nei[1]-1 not in possible_neighbors and horiz_nei[1]-1 not in state.board.board_nums:
                                possible_neighbors.append(horiz_nei[1]-1)
                        else:
                            if horiz_nei[1]-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if horiz_nei[0] == 0 or horiz_nei[0] == horiz_nei[1]-2:
                                        if horiz_nei[1]-1 not in possible_neighbors and horiz_nei[1]-1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[1]-1)
                                
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if vert_nei[0] == 0 or vert_nei[0] == horiz_nei[1]-2:
                                        if horiz_nei[1]-1 not in possible_neighbors and horiz_nei[1]-1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[1]-1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if vert_nei[1] == 0 or vert_nei[1] == horiz_nei[1]-2:
                                        if horiz_nei[1]-1 not in possible_neighbors and horiz_nei[1]-1 not in state.board.board_nums:
                                            possible_neighbors.append(horiz_nei[1]-1)
                    ##########################################################################################################################

                    ######################################################### BAIXO ##########################################################
                    if vert_nei[0] != None and not_unique:
                        # se for possivel seguir para baixo
                        ## MAIS UM ##
                        if vert_nei[0]+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if vert_nei[0]+1 not in possible_neighbors and vert_nei[0]+1 not in state.board.board_nums:
                                possible_neighbors.append(vert_nei[0]+1)
                        else:
                            if vert_nei[0]+1 < len(board)*len(board) and vert_nei[0]+1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if horiz_nei[0] == 0 or horiz_nei[0] == vert_nei[0]+2:
                                        if vert_nei[0]+1 not in possible_neighbors and vert_nei[0]+1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[0]+1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if horiz_nei[1] == 0 or horiz_nei[1] == vert_nei[0]+2:
                                        if vert_nei[0]+1 not in possible_neighbors and vert_nei[0]+1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[0]+1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if vert_nei[1] == 0 or vert_nei[1] == vert_nei[0]+2:
                                        if vert_nei[0]+1 not in possible_neighbors and vert_nei[0]+1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[0]+1)
                        ## MENOS UM ##
                        if vert_nei[0]-1 == 1:
                            # se o valor a colocar for o primeiro
                            if vert_nei[0]-1 not in possible_neighbors and vert_nei[0]-1 not in state.board.board_nums and vert_nei[0]-1 not in state.board.board_nums:
                                possible_neighbors.append(vert_nei[0]-1)
                        else:
                            if vert_nei[0]-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if horiz_nei[0] == 0 or horiz_nei[0] == vert_nei[0]-2:
                                        if vert_nei[0]-1 not in possible_neighbors and vert_nei[0]-1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[0]-1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if horiz_nei[1] == 0 or horiz_nei[1] == vert_nei[0]-2:
                                        if vert_nei[0]-1 not in possible_neighbors and vert_nei[0]-1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[0]-1)
                                    
                                # para CIMA
                                if vert_nei[1] != None:
                                    if vert_nei[1] == 0 or vert_nei[1] == vert_nei[0]-2:
                                        if vert_nei[0]-1 not in possible_neighbors and vert_nei[0]-1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[0]-1)
                    ##########################################################################################################################

                    ########################################################## CIMA ##########################################################
                    if vert_nei[1] != None and not_unique:
                        # se for possivel seguir para baixo
                        ## MAIS UM ##
                        if vert_nei[1]+1 == len(board)*len(board):
                            # se o valor a colocar for o último
                            if vert_nei[1]+1 not in possible_neighbors and vert_nei[1]+1 not in state.board.board_nums:
                                possible_neighbors.append(vert_nei[1]+1)
                        else:
                            if vert_nei[1]+1 < len(board)*len(board) and vert_nei[1]+1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if horiz_nei[0] == 0 or horiz_nei[0] == vert_nei[1]+2:
                                        if vert_nei[1]+1 not in possible_neighbors and vert_nei[1]+1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[1]+1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if horiz_nei[1] == 0 or horiz_nei[1] == vert_nei[1]+2:
                                        if vert_nei[1]+1 not in possible_neighbors and vert_nei[1]+1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[1]+1)
                                    
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if vert_nei[0] == 0 or vert_nei[0] == vert_nei[1]+2:
                                        if vert_nei[1]+1 not in possible_neighbors and vert_nei[1]+1 not in state.board.board_nums:
                                            possible_neighbors.append(vert_nei[1]+1)
                        ## MENOS UM ##
                        if vert_nei[1]-1 == 1:
                            # se o valor a colocar for o primeiro
                            if vert_nei[1]-1 not in possible_neighbors and vert_nei[1]-1 not in state.board.board_nums :
                                possible_neighbors.append(vert_nei[1]-1)
                        else:
                            if vert_nei[1]-1 > 1:
                                # caso não seja devo verificar se terá continuação possivel
                                # pela ESQUERDA
                                if horiz_nei[0] != None:
                                    if horiz_nei[0] == 0 or horiz_nei[0] == vert_nei[1]-2:
                                        if vert_nei[1]-1 not in possible_neighbors and vert_nei[1]-1 not in state.board.board_nums :
                                            possible_neighbors.append(vert_nei[1]-1)
                                
                                # pela DIREITA
                                if horiz_nei[1] != None:
                                    if horiz_nei[1] == 0 or horiz_nei[1] == vert_nei[1]-2:
                                        if vert_nei[1]-1 not in possible_neighbors and vert_nei[1]-1 not in state.board.board_nums :
                                            possible_neighbors.append(vert_nei[1]-1)
                                    
                                # para BAIXO
                                if vert_nei[0] != None:
                                    if vert_nei[0] == 0 or vert_nei[0] == vert_nei[1]-2:
                                        if vert_nei[1]-1 not in possible_neighbors and vert_nei[1]-1 not in state.board.board_nums :
                                            possible_neighbors.append(vert_nei[1]-1)
                    ##########################################################################################################################
                    if possible_neighbors == []:
                        if horiz_nei[0] != 0 and horiz_nei[1] != 0 and vert_nei[0] != 0 and vert_nei[1] != 0:
                            return []
                    for x in possible_neighbors:
                        if self.valid_manhattan(state, x, i, j) and self.free_neighbors(state, x, i, j):
                            actions.append((i+1,j+1,x))
        # print("\nActions:\n"s, actions)
        self.uni_actions= actions
        best_actions = self.return_best_actions(actions, len(board))
        return best_actions
   
    def free_neighbors (self, state: NumbrixState, num: int, row: int, col: int):
        esquerda = True
        direita = True
        cima = True
        baixo = True
        board = state.board.board
        ## Esquerda
        if col-1 >= 0:
            ## tem vizinho à esquerda
            left_nei = board[row][col-1]
            if left_nei != 0:
                horiz_nei = list(state.board.adjacent_horizontal_numbers(row+1, col))
                vert_nei = list(state.board.adjacent_vertical_numbers(row+1, col))
                neighbors = (horiz_nei[0], num, vert_nei[0], vert_nei[1])
                if left_nei == 1:
                    # nao tem anterior
                    if left_nei+1 not in neighbors and neighbors.count(0) < 1:
                        esquerda = False
                if left_nei == len(board)*len(board):
                    # nao tem seguinte
                    if left_nei-1 not in neighbors and neighbors.count(0) < 1:
                        esquerda = False
                if left_nei != 1 and left_nei != len(board)*len(board):
                    if left_nei+1 not in neighbors and left_nei-1 not in neighbors and neighbors.count(0) < 2:
                        esquerda = False
                    if left_nei+1 not in neighbors and left_nei-1 in neighbors and neighbors.count(0) < 1:
                        esquerda = False
                    if left_nei+1  in neighbors and left_nei-1 not in neighbors and neighbors.count(0) < 1:
                        esquerda = False
        
        ## Direita
        if col+1 < len(board):
            ## tem vizinho à direita
            right_nei = board[row][col+1]
            if right_nei != 0:
                horiz_nei = list(state.board.adjacent_horizontal_numbers(row+1, col+2))
                vert_nei = list(state.board.adjacent_vertical_numbers(row+1, col+2))
                neighbors = (num, horiz_nei[1], vert_nei[0], vert_nei[1])
                if right_nei == 1:
                    # nao tem anterior
                    if right_nei+1 not in neighbors and neighbors.count(0) < 1:
                        direita = False
                if right_nei == len(board)*len(board):
                    # nao tem seguinte
                    if right_nei-1 not in neighbors and neighbors.count(0) < 1:
                        direita = False
                if right_nei != 1 and right_nei != len(board)*len(board):
                    if right_nei+1 not in neighbors and right_nei-1 not in neighbors and neighbors.count(0) < 2:
                        direita = False
                    if right_nei+1 not in neighbors and right_nei-1 in neighbors and neighbors.count(0) < 1:
                        direita = False
                    if right_nei+1  in neighbors and right_nei-1 not in neighbors and neighbors.count(0) < 1:
                        direita = False
        
        ## Baixo
        if row+1 < len(board):
            ## tem vizinho em baixo
            bottom_nei = board[row+1][col]
            if bottom_nei != 0:
                horiz_nei = list(state.board.adjacent_horizontal_numbers(row+2, col+1))
                vert_nei = list(state.board.adjacent_vertical_numbers(row+2, col+1))
                neighbors = (horiz_nei[0], horiz_nei[1], vert_nei[0], num)
                if bottom_nei == 1:
                    # nao tem anterior
                    if bottom_nei+1 not in neighbors and neighbors.count(0) < 1:
                        baixo = False
                if bottom_nei == len(board)*len(board):
                    # nao tem seguinte
                    if bottom_nei-1 not in neighbors and neighbors.count(0) < 1:
                        baixo = False
                if bottom_nei != 1 and bottom_nei != len(board)*len(board):
                    if bottom_nei+1 not in neighbors and bottom_nei-1 not in neighbors and neighbors.count(0) < 2:
                        baixo = False
                    if bottom_nei+1 not in neighbors and bottom_nei-1 in neighbors and neighbors.count(0) < 1:
                        baixo = False
                    if bottom_nei+1  in neighbors and bottom_nei-1 not in neighbors and neighbors.count(0) < 1:
                        baixo = False
        
        ## Cima
        if row-1 >= 0:
            ## tem vizinho em cima
            upper_nei = board[row-1][col]
            if upper_nei != 0:
                horiz_nei = list(state.board.adjacent_horizontal_numbers(row, col+1))
                vert_nei = list(state.board.adjacent_vertical_numbers(row, col+1))
                neighbors = (horiz_nei[0], horiz_nei[1], num, vert_nei[1])
                if upper_nei == 1:
                    # nao tem anterior
                    if upper_nei+1 not in neighbors and neighbors.count(0) < 1:
                        cima = False
                if upper_nei == len(board)*len(board):
                    # nao tem seguinte
                    if upper_nei-1 not in neighbors and neighbors.count(0) < 1:
                        cima = False
                if upper_nei != 1 and upper_nei != len(board)*len(board):
                    if upper_nei+1 not in neighbors and upper_nei-1 not in neighbors and neighbors.count(0) < 2:
                        cima = False
                    if upper_nei+1 not in neighbors and upper_nei-1 in neighbors and neighbors.count(0) < 1:
                        cima = False
                    if upper_nei+1  in neighbors and upper_nei-1 not in neighbors and neighbors.count(0) < 1:
                        cima = False
        return esquerda and direita and baixo and cima

    def get_manhattan_distance(self, pos1X: int, pos1Y: int, pos2X: int, pos2Y: int):
        """ Recebe como input a posição duas posições e calcula a distancia
        de manhattan até à mesma"""
        return int(abs(pos1X-pos2X)+abs(pos1Y-pos2Y))

    def valid_manhattan(self, state: NumbrixState, num:int, row: int, col: int):
        board_cells = state.board.board_cells
        # print(board_cells)
        for cell in board_cells:
            if cell[2] != 0 and cell[2] != num:
                if self.get_manhattan_distance(row, col, cell[0]-1, cell[1]-1) > abs(num-cell[2]):
                        return False
        return True

    def select_next_action(self, actions, size):
        selected_actions = []
        index = 0
        # conta o número de ações para determinado valor
        freq = [0] * size
        for action in actions:
            freq[action[2]-1]+=1
        
        for i in range (len(freq)):
            if freq[i] != 0:
                current_min = freq[i]
                # pega no primeiro diferente de zero
                break;
        
        for i in range (len(freq)):
            if freq[i] != 0 and freq[i] < current_min:
                current_min = freq[i]
                # encontra o verdadeiro min

        # retorna o index da action do valor com menos frequência
        for i in range (len(freq)):
            if freq[i] != 0 and freq[i] == current_min:
                index = i
        
        for action in actions:
            if action[2] == index+1:
                selected_actions.append(action)
        return selected_actions

    def return_best_actions(self, actions, size):
        best_actions = []
        # conta o número de ações para determinado valor
        freq = [0] * size*size
        for action in actions:
            freq[action[2]-1]+=1
        
        for i in range (len(freq)):
            if freq[i] != 0:
                current_min = freq[i]
                # pega no primeiro diferente de zero
                break;
        
        for i in range (len(freq)):
            if freq[i] != 0 and freq[i] < current_min:
                current_min = freq[i]
                # encontra o verdadeiro min

        # retorna o index da action do valor com menos frequência
        for i in range (len(freq)):
            if freq[i] != 0 and freq[i] == current_min:
                index = i
        
        for action in actions:
            if action[2] == index+1:
                best_actions.append(action)
        
        return best_actions

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        boardAux = Board()
        boardAux.initializeBoard(state.board.board, state.board.board_nums, state.board.board_cells)
        new_state = NumbrixState(boardAux)
        if action != ():
            row = action[0]
            col = action[1]
            nmbr = action[2]
            new_state.board.board[row-1][col-1] = nmbr
            new_state.board.board_nums.append(nmbr)
            new_state.board.board_cells.append((row, col, nmbr))
        return new_state

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        for i in range (len(state.board.board)):
            for j in range (len(state.board.board)):
                if int(state.board.board[i][j]) == 0:
                    return False
        return True


    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """        
        size = node.state.board.boardSize
        best_actions = self.select_next_action(self.uni_actions, size*size)
        selected_action = []
        board_freq = []
        min_row = 0
        min_col = 0
        current_min = 0

        # conta o número de ações para determinado valor
        freq = [0] * size * size
        for action in self.uni_actions:
            freq[action[2]-1]+=1

        for i in range (size):
            row = []
            for j in range (size):
                row.append(0)
            board_freq.append(row)
        
        #criar "board" com frequencias, ver qual tem menor e diferente de zero
        for action in best_actions:
            board_freq[action[0]-1][action[1]-1]+=1
        
        for i in range (size):
            for j in range (size):
                if current_min == 0 and board_freq[i][j] != 0:
                    current_min = board_freq[i][j]
                    min_row = i
                    min_col = j
                else:
                    if board_freq[i][j] < current_min and board_freq[i][j] != 0:
                        current_min = board_freq[i][j]
                        min_row = i
                        min_col = j
        
        for action in best_actions:
            if action[0]-1 == min_row and action[1]-1 == min_col:
                selected_action.append(action)
        if node.action in selected_action:
            return freq[node.action[2]-1]
        else:
            return 100
    
###################################################################################################
#                                             MAIN                                                #
###################################################################################################
if __name__ == "__main__":

    ### Exemplo 4 ###
    board = Board.parse_instance(sys.argv[1])

    problem = Numbrix(board)
    
    goal_node = depth_first_tree_search(problem)

    print(goal_node.state.board.to_string(), sep="")

    pass
