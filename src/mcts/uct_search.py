import random
import numpy as np
from .game import Game 


class UCTNode:

    def __init__(
        self, action, parent=None, board_state=None, is_terminal=False, node_value=0
    ):
        self.node_value = node_value
        self.board_state = board_state
        self.action = action
        self.parent = parent
        self.children = {}
        self.visits = 0
        self.reward = 0
        self.is_terminal = is_terminal

    def backpropagate(self, reward) -> None:
        self.visits += 1
        self.reward += reward
        if self.parent:
            self.parent.backpropagate(-reward)

    def expand(self) -> "UCTNode":
        valid_actions = self.board_state.get_moves()
        if len(self.children) != len(valid_actions):

            explored_actions = self.children.keys()
            unexplored_actions = [
                action for action in valid_actions if action not in explored_actions
            ]
            unexplored_action = random.choice(unexplored_actions)

            game = self.board_state.clone()
            _, reward, finished, _ = game.step(unexplored_action)
            new_child = UCTNode(unexplored_action, self, game, finished, reward[0])

            self.children[unexplored_action] = new_child
            return new_child
        elif not self.is_terminal:
            return self.best_child().expand()
        else:
            return self

    def ucb_score(self, exploration_weight=1) -> float:
        if self.visits == 0:
            return float("inf")  # shouldn't this be negative infinity?
        avg_reward = self.reward / self.visits
        exploration_term = exploration_weight * np.sqrt(
            np.log(self.parent.visits) / self.visits
        )
        return avg_reward + exploration_term

    def best_child(self) -> "UCTNode":
        return max(self.children.values(), key=lambda x: x.ucb_score())

    def rollout(self) -> int:
        """
        We only care about the 1st players reward
        """
        if self.is_terminal:
            return self.node_value

        game = self.board_state.clone()
        finished = False
        reward = None

        while not finished:
            action = random.choice(game.get_moves())
            _, reward, finished, _ = game.step(action)

        return reward[0]


class UCTSearch:

    def __init__(self, rollouts: int, game: Game):
        self.game = game
        self.rollouts = rollouts
        self.root = UCTNode(None, None, game)

    def determine_next_move(self) -> int:

        for _ in range(self.rollouts):
            node = self.root.expand()
            reward = node.rollout()
            node.backpropagate(reward)

        if self.root.is_terminal:
            return self.root.action

        return self.root.best_child().action

    def update(self, action, game, finished, reward) -> None:
        if action in self.root.children:
            self.root = self.root.children[action]
        else:
            new_node = UCTNode(action, self.root, game.clone(), finished, reward)
            self.root.children[action] = new_node
            self.root = new_node
