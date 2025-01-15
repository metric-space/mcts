import pytest
from mcts.game import Game
from mcts.uct_search import UCTSearch

from gym_connect4.envs import Connect4Env


class Connect4Game(Game):

    def __init__(self, game = Connect4Env()):
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


def test_mcts_expansion():
    """Test that the Monte Carlo Search Tree expands correctly."""
    game = Connect4Game()
    tree = UCTSearch(7, game.clone())
    tree.determine_next_move()
    assert len(tree.root.children) == 7
