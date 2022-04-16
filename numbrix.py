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
    
    def to_string(self):
        board_str=""
        for i in range (len(self.board)):
            for j in range (len(self.board)):
                board_str += str(self.board[i][j])
                if j < len(self.board)-1:
                    board_str += " "
            if i < len(self.board)-1:
                board_str += "\n"
        return board_str


###################################################################################################
#                                            NUMBRIX                                              #
###################################################################################################
class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        self.initial = NumbrixState(board)

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. 
        RETURN: [(linha, coluna, valor),(linha, coluna, valor),(linha, coluna, valor), ...]"""
        board = state.board.board
        print("\nBoard:\n", state.board.to_string())
        numbers = [0]*len(board)*len(board)
        print(numbers)
        actions = []

        for i in range (len(board)):
            for j in range (len(board)):
                if board[i][j] != 0:
                    numbers[board[i][j]-1] = board[i][j]
        
        # for i in range (len(board)):
        #     for j in range (len(board)):
        #         if 
        print(numbers)
               
        # print("\nActions:\n", actions)
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
    problem = Numbrix(board)

    # Usar uma técnica de procura para resolver a instância,
    goal_node = depth_first_tree_search(problem)

    # Retirar a solução a partir do nó resultante,

    # Imprimir para o standard output no formato indicado.
    print("Solution:\n", goal_node.state.board.to_string(), sep="")

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
    # board = Board.parse_instance(sys.argv[1])

    # problem = Numbrix(board)

    # goal_node = astar_search(problem)

    # print("Is goal?", problem.goal_test(goal_node.state))
    # print("Solution:\n", goal_node.state.board.to_string(), sep="")
    pass
