from mcts import *


def final_move_test():
    MAXIMUM_MCTS_ITERATIONS = 20000
    game_state = ['x', 'o', 'o', 'o', 'o', 'x', 'x', 'x', '_']
    active_player = 'x'

    game_state, active_player, _ = monte_carlo_tree_search(
        game_state, active_player, MAXIMUM_MCTS_ITERATIONS)
    print(game_state)
    assert game_state == ['x', 'o', 'o', 'o', 'o', 'x', 'x', 'x', 'x']


def easy_x_win_test():
    MAXIMUM_MCTS_ITERATIONS = 20000
    game_state = ['x', 'o', 'x', 'o', 'o', '_', '_', '_', 'x']
    active_player = 'x'

    game_state, active_player, previous_action = monte_carlo_tree_search(
        game_state, active_player, MAXIMUM_MCTS_ITERATIONS)
    print(previous_action)
    print(game_state)
    # assert game_state == ['x', 'o', 'x', 'o', 'o', '_', '_', '_', 'x']


def optimal_tree_test():
    game_state = ['x', 'o', 'x', 'o', 'o', '_', '_', '_', 'x']
    active_player = 'x'
    tree = get_optimal_tree(game_state, active_player)
    print(tree.win_frequency)
    print([
        f'Active player: {child.active_player}, win frequency: {child.win_frequency}, action = {child.previous_action}'
        for child in tree.children
    ])


random.seed(11)
optimal_tree_test()
