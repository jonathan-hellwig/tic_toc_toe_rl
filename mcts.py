from typing import Optional
import typing
from tic_toc_toe import *
import random


class MCTSNode:
    children: list['MCTSNode']
    previous_action: Optional[int]
    game_state: list[str]
    active_player: str
    win_frequency: float
    outcomes: typing.Dict[str, int]
    parent: 'MCTSNode'

    def __init__(self, game_state, active_player, parent,
                 previous_action) -> None:
        self.previous_action = previous_action
        self.parent = parent
        self.children = []
        self.game_state = game_state
        self.active_player = active_player
        self.outcomes = {'x won': 0, 'o won': 0, 'draw': 0}

    def __repr__(self) -> str:
        return self.game_state.__str__()

    @property
    def win_frequency(self):
        # In some cases there is no distinction between draws and wins
        # TODO: Use -+1 reward at this point
        total = self.outcomes['x won'] + self.outcomes[
            'o won'] + self.outcomes['draw']
        if total == 0:
            return 0
        if self.active_player == 'x':
            return self.outcomes['x won'] / total
        else:
            return self.outcomes['o won'] / total


def select_node(node: MCTSNode,
                random_selection_probability: float = 0.1) -> MCTSNode:
    # Select a node according to the tree policy

    # Each node can be selected at random or greedily
    current_node = node
    while True:
        if not current_node.children:
            return current_node
        if get_available_actions(node.game_state):
            selectable_notes = [current_node] + current_node.children
        else:
            selectable_notes = current_node.children
        if random.random() < random_selection_probability:
            selected_node = random.choice(selectable_notes)
        else:
            selected_node = max(selectable_notes,
                                key=lambda x: x.win_frequency)
        if selected_node == current_node:
            return selected_node
        else:
            current_node = selected_node


def expand_tree(node: MCTSNode,
                maximum_number_of_expansions: int = 1) -> list[MCTSNode]:
    # Random selection of new nodes
    # In Browne at al., 2012 the algorithms expands nodes as long as there are unexplored nodes
    # The implementation below sampled from the set of unexplored and explored nodes equally
    if get_outcome(node.game_state) != 'ongoing':
        return node.children
    explored_actions = [child.previous_action for child in node.children]
    unexplored_actions = [
        action for action in get_available_actions(node.game_state)
        if action not in explored_actions
    ]
    number_of_expansions = min(maximum_number_of_expansions,
                               len(unexplored_actions))
    random_actions = random.sample(unexplored_actions, number_of_expansions)
    new_children = []
    for action in random_actions:
        game_state, active_player = set_action(node.game_state,
                                               node.active_player, action)
        new_node = MCTSNode(game_state, active_player, node, action)
        node.children.append(new_node)
        new_children.append(new_node)
    return new_children


def sample(new_children: list[MCTSNode]) -> list[str]:
    # Sample action according to a default policy
    outcomes = []
    for child in new_children:
        while True:
            reward = get_outcome(child.game_state)
            if reward != 'ongoing':
                outcomes.append(reward)
                break
            available_actions = get_available_actions(child.game_state)
            action = random.choice(available_actions)
            game_state, active_player = set_action(child.game_state,
                                                   child.active_player, action)
            child = MCTSNode(game_state, active_player, None, None)
    return outcomes


def back_propagate_value(new_node: MCTSNode, outcome: str):
    current_node = new_node
    while True:
        current_node.outcomes[outcome] += 1
        if current_node.parent is None:
            break
        current_node = current_node.parent


def get_optimal_tree(game_state: list[str], active_player: str):
    root_node = MCTSNode(game_state, active_player, None, None)
    stack = [root_node]
    while True:
        current_node = stack.pop()
        for action in get_available_actions(current_node.game_state):
            game_state, active_player = set_action(current_node.game_state,
                                                   current_node.active_player,
                                                   action)
            new_child = MCTSNode(game_state, active_player, current_node,
                                 action)
            current_node.children.append(new_child)
            outcome = get_outcome(new_child.game_state)
            if outcome != 'ongoing':
                back_propagate_value(new_child, outcome)
            else:
                stack.append(new_child)

        if not stack:
            break
    return root_node


def monte_carlo_tree_search(
        game_state: list[str], active_player: str,
        maximum_iterations: int) -> tuple[list[str], str, int]:
    root_node = MCTSNode(game_state, active_player, None, None)
    for _ in range(maximum_iterations):
        selected_node = select_node(root_node)
        new_children = expand_tree(selected_node)
        outcomes = sample(new_children)
        for child, outcome in zip(new_children, outcomes):
            back_propagate_value(child, outcome)
    if get_outcome(root_node.game_state) != 'ongoing':
        return None, None, None
    best_child = min(root_node.children, key=lambda x: x.win_frequency)
    return best_child.game_state, best_child.active_player, best_child.previous_action


def main():
    random.seed(1)

    MAXIMUM_MCTS_ITERATIONS = 200
    game_state = ['_'] * 9
    active_player = 'x'

    while True:
        game_state, active_player, _ = monte_carlo_tree_search(
            game_state, active_player, MAXIMUM_MCTS_ITERATIONS)
        if get_outcome(game_state) != 'ongoing':
            break
        print(to_string(game_state))
        print("Enter your move: ")
        action = int(input())
        game_state, active_player = set_action(game_state, active_player,
                                               action)
        if get_outcome(game_state) != 'ongoing':
            break
    print(to_string(game_state))
    print(get_outcome(game_state))


if __name__ == "__main__":
    main()
