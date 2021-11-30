from Game import *
from MCTS import *

N_SWEEPS = 1000

# np.random.seed(1234)
state = GameState()
state.new_game()
mcts = MCTS(state, c_param=1.)
print("STARTING BOARD:\n")
print_board(state.get_board())

user = input ("\nInsert 1 to play first, 2 to play second, anything else to watch the AI play: ")
if user.isdigit():
    user = int(user)
    if user==2:
        user = -1

turn = 1
while not state.is_game_over():
    player = state.get_player()
    print('\nMOVE %d\n' % (turn))

    for n in range(N_SWEEPS):
        mcts.sweep()

    # mcts.print_moves_statistics()

    if player==user:
        legal_actions = state.get_legal_actions()
        print('Legal moves: ', legal_actions)
        move = input ("Make your move: ")
        if not move.isdigit():
            move = -1
        move = int(move)
        while move not in legal_actions:
            move = input ("Make your move: ")
            if not move.isdigit():
                move = -1
            move = int(move)
        idx, = np.where(legal_actions == move)
        idx=idx[0]
        state = state.move(move)
        for child in mcts.root.children:
            if state == child.state and move==child.parent_action:
                mcts.play_move(child)
    else:
        mcts.play_best_move()
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
