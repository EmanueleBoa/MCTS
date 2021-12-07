import numpy as np

class GameState (object):
    def __init__ (self, board=np.zeros((6,7), dtype=np.int8), player=1):
        self.board =  board
        self.player = player

    def new_game(self):
        self.board = np.zeros((6,7), dtype=np.int8)
        self.player = 1

    def get_legal_actions(self):
        actions = []
        if not self.is_game_over():
            actions = [i for i in range(7) if self.board[-1,i]==0]
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
        board = self.board
        # check rows
        for i in range(6):
            for j in range(4):
                value = int(np.sum(board[i,j:j+4])/4)
                if np.absolute(value) == 1:
                    return value
        # check columns
        for j in range(7):
            for i in range(3):
                value = int(np.sum(board[i:i+4,j])/4)
                if np.absolute(value) == 1:
                    return value
        # check diagonals 1
        for i in range(3):
            for j in range(4):
                diag = [board[i+k, j+k] for k in range(4)]
                value = int(np.sum(diag)/4)
                if np.absolute(value) == 1:
                    return value
        # check diagonals 2
        board = board[:,::-1]
        for i in range(3):
            for j in range(4):
                diag = [board[i+k, j+k] for k in range(4)]
                value = int(np.sum(diag)/4)
                if np.absolute(value) == 1:
                    return value
        # otherwise it's a tie
        return 0

    def move(self, action):
        board = np.copy(self.board)
        idx, = np.where(board[:,action] == 0)
        board[idx[0], action] = self.player
        player = -1*self.player
        return GameState(board, player)

    def select_random_action(self):
        return np.random.choice(self.get_legal_actions())

    def simulate_random_game(self):
        current_state = self
        while not current_state.is_game_over():
            action = current_state.select_random_action()
            current_state = current_state.move(action)
        return current_state.game_result()

    def get_board(self):
        return self.board

    def get_player(self):
        return self.player

    def to_string(self):
        symbol = {1: 'x', -1: 'o', 0: ' '}
        board = self.board[::-1,:]
        string = ' 0 1 2 3 4 5 6 \n'
        for row in board:
            string += '|'
            for el in row:
                string += symbol[el] + '|'
            string += '\n'
        return string

    def encode(self):
        return self.board*self.player

    def __eq__(self, other):
        return ((np.array_equal(self.board, other.board)) and (self.player == other.player))

    def __ne__(self, other):
        return not self.__eq__(other)
