# TODO: Replace all occurences of strings with enums
import copy


def get_available_actions(game_state) -> list[int]:
    return [i for i in range(9) if game_state[i] == '_']


def set_action(game_state: list[str], active_player: str,
               action: int) -> tuple[list[str],str]:
    if not action in get_available_actions(game_state):
        return
    game_state = copy.copy(game_state)
    if active_player == 'x':
        game_state[action] = 'x'
        active_player = 'o'
    else:
        game_state[action] = 'o'
        active_player = 'x'
    return game_state, active_player


def get_outcome(game_state) -> str:
    pairs_of_three = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7],
                      [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    for pair_of_three in pairs_of_three:
        current_pair = [game_state[i] for i in pair_of_three]
        if current_pair[0] != '_' and current_pair[0] == current_pair[
                1] and current_pair[1] == current_pair[2]:
            if current_pair[0] == 'x':
                return 'x won'
            else:
                return 'o won'
    if all(x != '_' for x in game_state):
        return 'draw'
    return 'ongoing'


def to_string(game_state) -> str:
    return ','.join(game_state[0:3]) + '\n' + ','.join(
        game_state[3:6]) + '\n' + ','.join(game_state[6:9])
