import numpy as np

class GameState (object):
    def __init__ (self, board=np.zeros(9, dtype=np.int8), player=1):
        self.board =  board
        self.player = player

    def new_game(self):
        self.board = np.zeros(9, dtype=np.int8)
        self.player = 1

    def get_legal_actions(self):
        actions = []
        if not self.is_game_over():
            actions, = np.where(self.board==0)
        return actions

    def is_game_over(self):
        # check if board is full
        if 0 not in self.board:
            return True
        # check if anyone won
        elif self.game_result() != 0:
            return True
        return False

#     def game_result(self):
#         board = self.board.reshape((3,3))
#         # check rows
#         for i in range(3):
#             value = int(np.sum(board[i,:])/3)
#             if np.absolute(value) == 1:
#                 return value
#         # check columns
#         for i in range(3):
#             value = int(np.sum(board[:,i])/3)
#             if np.absolute(value) == 1:
#                 return value
#         # check diagonal 1
#         value = int((board[0][0] + board[1][1] + board[2][2])/3)
#         if np.absolute(value) == 1:
#             return value
#         # check diagonal 2
#         value = int((board[0][2] + board[1][1] + board[2][0])/3)
#         if np.absolute(value) == 1:
#             return value
#         # otherwise it's a tie
#         return 0

    def game_result(self):
        winningLines = np.array([[0,1,2],[3,4,5],[6,7,8],[0,3,6],[1,4,7],[2,5,8],[0,4,8],[2,4,6]])
        board = self.board
        for line in winningLines:
            if len(set(board[line])) == 1:
                return board[line][0]
        return 0


    def move(self, action):
        board = np.copy(self.board)
        board[action] = self.player
        player = -1*self.player
        return GameState(board, player)

    def select_random_action(self):
        return np.random.choice(self.get_legal_actions())

    def get_board(self):
        return self.board

    def get_player(self):
        return self.player

    def __eq__(self, other):
        return ((np.array_equal(self.board, other.board)) and (self.player == other.player))

    def __ne__(self, other):
        return not self.__eq__(other)

def print_board(board):
    board = board.reshape((3,3))
    symbol = {1: 'x', -1: 'o', 0: ' '}
    for row in board:
        print('|'+symbol[row[0]]+'|'+symbol[row[1]]+'|'+symbol[row[2]]+'|')
