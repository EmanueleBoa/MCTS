import numpy as np
from collections import defaultdict

class Node (object):
    def __init__ (self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        self.untried_actions = None
