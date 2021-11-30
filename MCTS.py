import numpy as np
from collections import defaultdict
import copy
from Game import *

class Node (object):
    def __init__ (self, state, parent=None, parent_action=None):
        self.state = state
        self.parent = parent
        self.parent_action = parent_action
        self.children = []
        self.number_of_visits = 0
        self.results = defaultdict(int)
        self.results[1] = 0
        self.results[-1] = 0
        self.results[0] = 0
        self.untried_actions = self.state.get_legal_actions()

    def n(self):
        return self.number_of_visits

    def reward(self):
        reward = (self.results[1]-self.results[-1])/self.n()
        return reward*self.parent.state.get_player()

    def is_terminal_node(self):
        return self.state.is_game_over()

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    def expand(self):
        action = self.untried_actions[0]
        self.untried_actions = self.untried_actions[1:]
        new_state = self.state.move(action)
        child = Node(new_state, parent=self, parent_action=action)
        self.children.append(child)
        return child

    def best_child(self, c_param=1.0):
        UCT = [(c.reward() + c_param*np.sqrt(2*np.log(self.n())/c.n())) for c in self.children]
        return self.children[np.argmax(UCT)]

    def most_visited_child(self):
        visits = [c.n() for c in self.children]
        return self.children[np.argmax(visits)]

    def backpropagate(self, result):
        self.number_of_visits += 1.
        self.results[result] += 1.
        if self.parent:
            self.parent.backpropagate(result)

    def tree_policy(self, c_param=1.0):
        current_node = self
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child(c_param)
        return current_node

    def rollout(self):
        return self.state.simulate_random_game()

    def print_children_statistics(self):
        actions = [c.parent_action for c in self.children]
        rewards = [c.reward() for c in self.children]
        visits = [c.n() for c in self.children]
        print('\nStats:')
        for i in range(len(actions)):
            print("- move: %2d  reward: %0.2f  visits: %4d" % (actions[i], rewards[i], visits[i]))
        print('\nSummary:')
        print("- highest reward: %2d" % (actions[np.argmax(rewards)]))
        print("- most visited:   %2d\n" % (actions[np.argmax(visits)]))


class MCTS (object):
    def __init__ (self, state, c_param=1.):
        self.root = Node(state)
        self.c_param = c_param

    def sweep(self):
        v = self.root.tree_policy(self.c_param)
        reward = v.rollout()
        v.backpropagate(reward)

    def best_move(self):
        return self.root.best_child(c_param=0.)

    def play_best_move(self):
        best_child = self.best_move()
        idx = self.root.children.index(best_child)
        self.root = self.root.children[idx]
        self.root.parent = None

    def play_move(self, state):
        idx = self.root.children.index(state)
        self.root = self.root.children[idx]
        self.root.parent = None

    def root_state(self):
        return self.root.state

    def print_moves_statistics(self):
        self.root.print_children_statistics()
