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
    in_board = []
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
    last_action = (0,0,0)

    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. 
        RETURN: [(linha, coluna, valor),(linha, coluna, valor),(linha, coluna, valor), ...]"""
        board = state.board.board
        print("\nBoard:\n", state.board.to_string())
        actions = []
        in_board = []
        domain = []
        possible_neighbors = []
        cel_actions = []
        for i in range (len(board)):
            for j in range (len(board)):
                if board[i][j] != 0:
                    in_board.append(board[i][j])

        for i in range (len(board)*len(board)):
            if i not in in_board and i != 0:
                domain.append(i)

        for i in range (len(board)):
            for j in range (len(board)):
                if board [i][j] == 0:
                    
                    print("FOR ==> ",(i,j))
                    not_unique = True
                    current_dom = copy.deepcopy(domain)
                    horiz_nei = list(state.board.adjacent_horizontal_numbers(i+1, j+1))
                    vert_nei = list(state.board.adjacent_vertical_numbers(i+1, j+1))
                    if horiz_nei[0] != None and horiz_nei[1] != None:
                        if horiz_nei[1] == horiz_nei[0]+2:
                            return [(i+1, j+1, horiz_nei[0]+1)]
                        if horiz_nei[1] == horiz_nei[0]-2:
                            return [(i+1, j+1, horiz_nei[0]-1)]
                    if vert_nei[0] != None and vert_nei[1] != None:
                        if vert_nei[1] == vert_nei[0]+2:
                            return [(i+1, j+1, vert_nei[0]+1)]
                        if vert_nei[1] == vert_nei[0]-2:
                            return [(i+1, j+1, vert_nei[0]-1)]
                    
                    if horiz_nei[0] != None and horiz_nei[0] != 0:
                        if horiz_nei[0]+1 not in possible_neighbors:
                            possible_neighbors.append(horiz_nei[0]+1)
                        if horiz_nei[0]-1 not in possible_neighbors:
                            possible_neighbors.append(horiz_nei[0]-1)
                    if horiz_nei[1] != None and horiz_nei[1] != 0:
                        if horiz_nei[1]+1 not in possible_neighbors:
                            possible_neighbors.append(horiz_nei[1]+1)
                        if horiz_nei[1]-1 not in possible_neighbors:
                            possible_neighbors.append(horiz_nei[1]-1)
                    if vert_nei[0] != None and vert_nei[0] != 0:
                        if vert_nei[0]+1 not in possible_neighbors:
                            possible_neighbors.append(vert_nei[0]+1)
                        if vert_nei[0]-1 not in possible_neighbors:
                            possible_neighbors.append(vert_nei[0]-1)
                    if vert_nei[1] != None and vert_nei[1] != 0:
                        if vert_nei[1]+1 not in possible_neighbors:
                            possible_neighbors.append(vert_nei[1]+1)
                        if vert_nei[1]-1 not in possible_neighbors:
                            possible_neighbors.append(vert_nei[1]-1)
                    # print("possible_neighbors: ", possible_neighbors)
                    print("current_dom (before): ", current_dom)
                    to_remove = []
                    for elem in current_dom:
                        if elem not in possible_neighbors:
                            if not self.valid_manhattan(state, elem, i, j) or not self.free_neighbors(state, elem, i, j):
                                to_remove.append(elem)
                    print("to remove: ", to_remove)
                    for fail in to_remove:
                        current_dom.remove(fail)
                    print("current_dom (after): ", current_dom)

                    for elem in current_dom:
                        actions.append((i+1, j+1, elem))
        # print("\nActions:\n", actions)
        cel_actions = self.select_next_actions(actions, len(board))
        print("\nCELL ACTIONS:\n", cel_actions)
        return cel_actions

    def check_extra(self, state: NumbrixState, possible_neighbors: list, row: int, col: int):
        board = state.board.board
        extra = []
        for i in range (len(board)*len(board)):
            if i != 0:
                if self.valid_manhattan(state, i, row, col) and self.free_neighbors(state, i, row, col) and i not in possible_neighbors:
                    extra.append(i)
        return extra

    def anyblocked(self, state: NumbrixState):
        board = state.board.board
        flag = True

        for i in range (len(board)):
            for j in range (len(board)):
                current = board[i][j]
                if flag == False:
                    return True
                if current != 0:
                    horiz_nei = list(state.board.adjacent_horizontal_numbers(i+1, j+1))
                    vert_nei = list(state.board.adjacent_vertical_numbers(i+1, j+1))
                    neighbors = (horiz_nei[0], horiz_nei[1], vert_nei[0], vert_nei[1])
                    if current == 1:
                        # nao tem anterior
                        if current+1 not in neighbors and neighbors.count(0) < 1:
                            flag = False
                    if current == len(board)*len(board):
                        # nao tem seguinte
                        if current-1 not in neighbors and neighbors.count(0) < 1:
                            flag = False
                    else:
                        if current+1 not in neighbors and current-1 not in neighbors and neighbors.count(0) < 2:
                            flag = False
                        if current+1 not in neighbors and current-1 in neighbors and neighbors.count(0) < 1:
                            flag = False
                        if current+1  in neighbors and current-1 not in neighbors and neighbors.count(0) < 1:
                            flag = False
        if flag == False:
            return True
        return False
    
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
        
    def get_coordinates(state: NumbrixState, num:int):
        for i in  range (len(state.board.board)):
            for j in range(len(state.board.board)):
                if num == state.board.board[i][j]:
                    coord = (i,j)
                    return coord
        return False

    def valid_manhattan(self, state: NumbrixState, num1:int, row: int, col: int):
        for i in  range (len(state.board.board)):
            for j in range(len(state.board.board)):
                if state.board.board[i][j] != 0 and state.board.board[i][j] != num1:
                    # print("Manhattan for ", num1, " and ", state.board.board[i][j])
                    if self.get_manhattan_distance(row, col, i, j) > abs(num1-state.board.board[i][j]):
                        return False
        # print("Manhattan for ", num1, " = TRUE")
        return True

    def select_next_actions(self, actions, size):
        selected_action = []
        board_freq = []
        min_row = 0
        min_col = 0
        current_min = 0
        # print("actions: ", actions)
        for i in range (size):
            row = []
            for j in range (size):
                row.append(0)
            board_freq.append(row)
        
        #criar "board" com frequencias, ver qual tem menor e diferente de zero
        for action in actions:
            board_freq[action[0]-1][action[1]-1]+=1
        
        # print(board_freq)

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
        
        for action in actions:
            if action[0]-1 == min_row and action[1]-1 == min_col:
                selected_action.append(action)
        
        # retornar ações para essa
        # print(selected_action)
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
            new_state.board.board[row-1][col-1] = nmbr
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
        return 1
    
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

    # # Ler o ficheiro de input de sys.argv[1],
    # board = Board.parse_instance(sys.argv[1])
    # problem = Numbrix(board)

    # # Usar uma técnica de procura para resolver a instância,
    # goal_node = depth_first_tree_search(problem)

    # # Retirar a solução a partir do nó resultante,

    # # Imprimir para o standard output no formato indicado.
    # print("Solution:\n", goal_node.state.board.to_string(), sep="")

    ### Exemplo 3 ###
    # board = Board.parse_instance(sys.argv[1])
    
    # problem = Numbrix(board)

    # s0 = NumbrixState(board)
    # print("Initial:\n", s0.board.to_string(), sep="")

    # s1 = problem.result(s0, (2, 2, 1))
    # s2 = problem.result(s1, (0, 2, 3))
    # s3 = problem.result(s2, (0, 1, 4))
    # s4 = problem.result(s3, (1, 1, 5))
    # s5 = problem.result(s4, (2, 0, 7))
    # s6 = problem.result(s5, (1, 0, 8))
    # s7 = problem.result(s6, (0, 0, 9))

    # print("Is goal?", problem.goal_test(s7))
    # print("Solution:\n", s7.board.to_string(), sep="")

    ### Exemplo 4 ###
    board = Board.parse_instance(sys.argv[1])

    problem = Numbrix(board)

    goal_node = astar_search(problem)

    print(goal_node.state.board.to_string(), sep="")
    pass
