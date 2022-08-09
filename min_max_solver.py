import math
from typing import Optional
import typing
from tic_toc_toe import *

value_mapping = {'x won': 1, 'o won': -1, 'draw': 0}


class Node:
    children: list['Node']
    game_state: list[str]
    active_player: str
    optimal_actions: Optional[int]
    action: Optional[int]

    def __init__(self, game_state, active_player, action):
        self.children = []
        self.game_state = game_state
        self.active_player = active_player
        self.optimal_actions = None
        self.action = action

    def __repr__(self) -> str:
        return self.game_state.__repr__()


def build_game_tree(initial_game_state) -> Node:
    game_state = initial_game_state
    active_player = 'x'
    tree = Node(game_state, active_player, None)
    stack = [tree]
    while stack:
        current_node = stack.pop()
        for action in get_available_actions(current_node.game_state):
            game_state, active_player = set_action(current_node.game_state,
                                                   current_node.active_player,
                                                   action)
            new_node = Node(game_state, active_player, action)
            if get_outcome(game_state) == 'ongoing':
                stack.append(new_node)
            current_node.children.append(new_node)

    return tree


def find(list, element):
    for i in range(len(list)):
        if list[i] == element:
            return i


def minmax(node: Node, maximizing_player: bool):
    if not node.children:
        # print(get_outcome(node.game_state))
        return value_mapping[get_outcome(node.game_state)]
    optimal_actions = []
    if maximizing_player:
        value = -math.inf
        for child in node.children:
            child_value = minmax(child, False)
            # print(f'child: {child}, value: {child_value}')
            if value < child_value:
                value = child_value
                optimal_actions = [child.action]
            elif value == child_value:
                value = child_value
                optimal_actions.append(child.action)
    else:
        value = math.inf
        for child in node.children:
            child_value = minmax(child, True)
            if value > child_value:
                value = child_value
                optimal_actions = [child.action]
            elif value == child_value:
                value = child_value
                optimal_actions.append(child.action)
    node.optimal_actions = optimal_actions
    return value

def main():
    game_state = ['_'] * 9
    # game_state = ['x', 'o', 'o', 'x', 'x', '_', '_', 'o', '_']
    # game_state = ['x', 'o', 'o', 'x', '_', '_', '_', '_', '_']
    tree = build_game_tree(game_state)
    minmax(tree, True)
    # print(tree.children[tree.optimal_index].game_state)

    while True:
        tree = tree.children[find(get_available_actions(tree.game_state),
                                tree.optimal_actions[0])]
        if get_outcome(tree.game_state) != 'ongoing':
            break
        print(to_string(tree.game_state))
        print("Enter your move: ")
        action = int(input())
        player_action_index = find(get_available_actions(tree.game_state), action)
        tree = tree.children[player_action_index]
        if get_outcome(tree.game_state) != 'ongoing':
            break
    print(to_string(tree.game_state))
    print(get_outcome(tree.game_state))

if __name__ == "__main__":
    main()
