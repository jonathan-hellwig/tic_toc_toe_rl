from min_max_solver import *
from mcts import *

random.seed(1)
MAXIMUM_ITERATIONS = 3200
# game_state = ['_'] * 9
# game_state = ['x', 'x', 'o', 'o', '_', '_', '_', '_', '_']
# game_state = ['x', 'o', 'x', 'o', 'o', '_', 'x', 'x', '_']
game_state = ['x', 'o', 'x', 'o', '_', '_', '_', '_', '_']

tree = build_game_tree(game_state)
minmax(tree, True)
total = 0
score = 0

stack = [tree]
while True:
    if total % 100 == 0:
        print(total)
    current_node = stack.pop()
    # Am I choosing the correct action to compare?
    # Currently, I do not evaluate the node at top
    _, _, action = monte_carlo_tree_search(current_node.game_state,
                                           current_node.active_player,
                                           MAXIMUM_ITERATIONS)
    if action is not None and len(get_available_actions(current_node.game_state)) > 1:
        # print(f'Game state: {current_node.game_state}')
        # print(f'MCTS action: {action}')
        # print(f'Optimal actions: {current_node.optimal_actions}')
        total += 1
        if action in current_node.optimal_actions:
            score += 1
    for child in current_node.children:
        stack.append(child)

    if not stack:
        break

print(score / total)
