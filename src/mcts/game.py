from abc import ABC, abstractmethod
from typing import Any, List, Tuple


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


