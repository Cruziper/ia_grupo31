# numbrix.py: Template para implementação do projeto de Inteligência Artificial 2021/2022.
# Devem alterar as classes e funções neste ficheiro de acordo com as instruções do enunciado.
# Além das funções e classes já definidas, podem acrescentar outras que considerem pertinentes.

# Grupo 31:
# 84721 Gonçalo Cruz
# 98789 António Cunha

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
    """ Representação interna de um tabuleiro de Numbrix. """
    
    def get_number(self, row: int, col: int) -> int:
        """ Devolve o valor na respetiva posição do tabuleiro. """
        return self[Board.findRow(row)][Board.findColumn(col)]
    
    def adjacent_vertical_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente abaixo e acima, 
        respectivamente. """
        if (row-1 >= 1):
            if(row+1 <= Board.boardSize):
                """ Se tiver casa imediatamente abaixo e acima
                Return: ([linha+1][coluna], [linha-1][coluna]) """
                return (int(self[Board.findRow(row+1)][Board.findColumn(col)]), int(self[Board.findRow(row-1)][Board.findColumn(col)]))
            else:
                """ Se tiver apenas casa imediatamente acima
                Return: (None, [linha-1][coluna]) """
                return (None, int(self[Board.findRow(row-1)][Board.findColumn(col)]))
        else:
            if(row+1 <= Board.boardSize):
                """ Se tiver apenas casa imediatamente abaixo
                Return: ([linha+1][coluna], None) """
                return (int(self[Board.findRow(row+1)][Board.findColumn(col)]), None)
    
    def adjacent_horizontal_numbers(self, row: int, col: int):
        """ Devolve os valores imediatamente à esquerda e à direita, 
        respectivamente. """
        if (col-1 >= 1):
            if(col+1 <= Board.boardSize):
                """ Se tiver casa imediatamente à esquerda e à direita
                Return: ([linha][coluna-1], [linha][coluna+1]) """
                return (int(self[Board.findRow(row)][Board.findColumn(col-1)]), int(self[Board.findRow(row)][Board.findColumn(col+1)]))
            else:
                """ Se tiver apenas casa imediatamente à esquerda
                Return: ([linha][coluna-1], None) """
                return (int(self[Board.findRow(row)][Board.findColumn(col-1)]), None)
        else:
            if(col <= Board.boardSize):
                """ Se tiver apenas casa imediatamente à direita
                Return: (None, [linha][coluna+1]) """
                return (None, int(self[Board.findRow(row)][Board.findColumn(col+1)]))
    
    @staticmethod    
    def parse_instance(filename: str):
        """ Lê o ficheiro cujo caminho é passado como argumento e retorna
        uma instância da classe Board. """
        board = []
        with open(filename, "r") as f:
            # index 0 --> N
            Board.boardSize = int(f.readline())
            for line in f:
                row = [column.strip() for column in line.split('\t')]
                board.append(row)
                    
        return board

    def findRow(row: int):
        """ devolve o valor do index da linha """
        return row-1
    
    def findColumn(col: int):
        """ devolve o valor do index da coluna """
        return col-1

###################################################################################################
#                                            NUMBRIX                                              #
###################################################################################################
class Numbrix(Problem):
    def __init__(self, board: Board):
        """ O construtor especifica o estado inicial. """
        # TODO
        pass

    def actions(self, state: NumbrixState):
        """ Retorna uma lista de ações que podem ser executadas a
        partir do estado passado como argumento. """
        # TODO
        pass

    def result(self, state: NumbrixState, action):
        """ Retorna o estado resultante de executar a 'action' sobre
        'state' passado como argumento. A ação a executar deve ser uma
        das presentes na lista obtida pela execução de 
        self.actions(state). """
        # TODO
        pass

    def goal_test(self, state: NumbrixState):
        """ Retorna True se e só se o estado passado como argumento é
        um estado objetivo. Deve verificar se todas as posições do tabuleiro 
        estão preenchidas com uma sequência de números adjacentes. """
        # TODO
        pass

    def h(self, node: Node):
        """ Função heuristica utilizada para a procura A*. """
        # TODO
        pass
    
    # TODO: outros metodos da classe


###################################################################################################
#                                             MAIN                                                #
###################################################################################################
if __name__ == "__main__":
    # TODO:
    # Ler o ficheiro de input de sys.argv[1],
    board = Board.parse_instance(sys.argv[1])
    print(Board.boardSize)
    print(board)

    vertical_numbers = Board.adjacent_vertical_numbers(board, 2, 3)
    print(vertical_numbers)

    horizontal_numbers = Board.adjacent_horizontal_numbers(board, 3, 3)
    print(horizontal_numbers)
    # Usar uma técnica de procura para resolver a instância,

    # Retirar a solução a partir do nó resultante,
    # Imprimir para o standard output no formato indicado.
    pass
