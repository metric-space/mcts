from abc import ABC, abstractmethod
from typing import Any, List, Tuple
from gym_connect4.envs import Connect4Env


class Game(ABC):
    @abstractmethod
    def get_moves(self) -> List[Any]:
        """
        Return a list of all legal actions.
        """
        pass

    @abstractmethod
    def step(self, action: Any) -> Tuple[Any]:
        """
        Return the new state after performing the action.
        """
        pass

    @abstractmethod
    def is_terminal(self) -> bool:
        """
        Check if the given state is a terminal (end) state.
        """
        pass

    @abstractmethod
    def clone(self) -> "Game":
        """
        Create a deep copy of the game state.
        """
        pass

    @abstractmethod
    def game_state(self) -> Any:
        """
        Return the current game state.
        """
        pass


class Connect4Game(Game):

    def __init__(self, game=None):
        self.env = game or Connect4Env()

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