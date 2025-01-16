import pytest
from mcts.game import Game
from mcts.uct_search import UCTSearch
from mcts.debug import depth, count_nodes, extract_information_from_tree
import random

from gym_connect4.envs import Connect4Env


class Connect4Game(Game):

    def __init__(self, game=Connect4Env()):
        self.env = game

    def get_moves(self):
        return self.env.get_moves()

    def step(self, action):
        return self.env.step(action)

    def is_terminal(self):
        return self.env.is_terminal()

    def clone(self):
        cloned_game = self.env.clone()
        return Connect4Game(cloned_game)

    def game_state(self):
        return (self.env.board, self.env.current_player)


def test_mcts_initialization():
    """Test that the Monte Carlo Search Tree initializes correctly."""
    game = Connect4Game()
    tree = UCTSearch(10, game.clone())
    assert tree is not None


def test_mcts_expansion_1():
    """Test that the Monte Carlo Search Tree expands correctly."""
    game = Connect4Game()
    tree = UCTSearch(7, game.clone())
    tree.determine_next_move()
    assert len(tree.root.children) == 7




def test_mcts_expansion_2():
    """Test that the Monte Carlo Search Tree expands correctly."""
    n = 24
    game = Connect4Game()
    tree = UCTSearch(n, game.clone())
    tree.determine_next_move()
    assert (
        (count_nodes(tree.root) == n + 1)
        and (len(tree.root.children) == 7)
        and (depth(tree.root) == 3)
    )

def test_mcts_expansion_3():
    """Test that the Monte Carlo Search Tree expands correctly."""
    n = 24
    game = Connect4Game()
    tree = UCTSearch(n, game.clone())
    tree.determine_next_move()
    children = tree.root.children
    children_count_distribution = [len(child.children) for child in children.values()]
    assert children_count_distribution == [3,3,3,3,3,3,3]

def test_information_gathering():
    """Test that the tree policy selects the correct node."""
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

    extracted_info = extract_information_from_tree(mcts.root)

    assert len(extracted_info) == 4