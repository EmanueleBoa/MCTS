from Game import *
from MCTS import *

# np.random.seed(1234)
state = GameState()
state.new_game()
mcts = MCTS(state, c_param=1.)
print("STARTING BOARD:\n")
print_board(state.get_board())

user = int(input ("Insert 1 to play first, 2 otherwise: "))
if user==2:
    user = -1

turn = 1
while not state.is_game_over():
    player = state.get_player()
    print('\nMOVE %d\n' % (turn))

    for n in range(1000):
        mcts.sweep()

    if player==user:
        legal_actions = state.get_legal_actions()
        print('Legal moves: ', legal_actions)
        move = int(input ("Make your move: "))
        while move not in legal_actions:
            move = int(input ("Make your move: "))
        idx, = np.where(legal_actions == move)
        idx=idx[0]
        state = state.move(move)
        for child in mcts.root.children:
            if state == child.state and move==child.parent_action:
                mcts.play_move(child)
    else:
        best_move = mcts.best_move()
        mcts.play_move(best_move)
        state = mcts.root_state()

    print_board(state.get_board())

    turn += 1

result = state.game_result()
if result==1:
    print('\nPlayer 1 won!')
elif result==-1:
    print('\nPlayer 2 won!')
else:
    print('\nThe game ended in a tie!')
