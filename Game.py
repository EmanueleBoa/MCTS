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

    def game_result(self):
        board = self.board.reshape((3,3))
        # check rows
        for i in range(3):
            value = int(np.sum(board[i,:])/3)
            if np.absolute(value) == 1:
                return value
        # check columns
        for i in range(3):
            value = int(np.sum(board[:,i])/3)
            if np.absolute(value) == 1:
                return value
        # check diagonal 1
        value = int((board[0][0] + board[1][1] + board[2][2])/3)
        if np.absolute(value) == 1:
            return value
        # check diagonal 2
        value = int((board[0][2] + board[1][1] + board[2][0])/3)
        if np.absolute(value) == 1:
            return value
        # otherwise it's a tie
        return 0

    def move(self, action):
        if action in self.get_legal_actions():
            self.board[action] = self.player
            self.player = -self.player
        else:
            print("ERROR: action passed to move is not legal!")

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
