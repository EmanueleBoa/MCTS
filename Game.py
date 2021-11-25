import numpy as np

class GameState (object):
    def __init__ (self, board=np.zeros(9, dtype=np.int8), player=1):
        self.board =  board
        self.player = player
