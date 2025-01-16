from mcts.uct_search import UCTSearch
from mcts.game import Connect4Game
import random


def singular_mcts_game():

    c4_game = Connect4Game()

    finished = False

    mcts = UCTSearch(50, c4_game.clone())

    while not finished:

        # our play
        action = mcts.determine_next_move()

        _, reward, finished, _ = c4_game.step(action)
        mcts.update(action, c4_game, finished, reward[0])

        # player 2
        if not finished:
            player_2_action = random.choice(c4_game.get_moves())
            _, reward, finished, _ = c4_game.step(player_2_action)
            mcts.update(player_2_action, c4_game, finished, reward[0])

    return reward[0]


def singular_random_game():

    c4_game = Connect4Game()

    finished = False

    while not finished:

        # our play
        _, reward, finished, _ = c4_game.step(random.choice(c4_game.get_moves()))

        # player 2
        if not finished:
            _, reward, finished, _ = c4_game.step(random.choice(c4_game.get_moves()))

    return reward[0]


def sim(game=singular_mcts_game, no=100):

    total = no
    wins = 0
    draws = 0

    for _ in range(no):
        outcome = game()
        if outcome == 1:
            wins += 1
        elif outcome == 0:
            draws += 0
        else:
            pass

    return {"total": total, "wins": wins, "draws": draws}


if __name__ == "__main__":

    c4_game = Connect4Game()

    finished = False

    mcts = UCTSearch(15, c4_game.clone())

    while not finished:

        # our play
        action = mcts.determine_next_move()

        _, reward, finished, _ = c4_game.step(action)
        mcts.update(action, c4_game, finished, reward[0])

        # player 2
        if not finished:
            player_2_action = random.choice(c4_game.get_moves())
            _, reward, finished, _ = c4_game.step(player_2_action)
            mcts.update(player_2_action, c4_game, finished, reward[0])

    # rendered_board = render_tree(mcts.root)
    ## save the rendered board to a file
    # with open("tree.html", "w") as file:
    #    file.write(rendered_board)

    outcome1 = sim(no=100)
    outcome2 = sim(game=singular_random_game, no=100)
    print(outcome1)
    print(outcome2)
