# Case 1, Moves=18, Opened=138158, Time=0.84
# Case 2, Moves=22, Opened=1440021, Time=8.55
# Case 3, Moves=24, Opened=4081243, Time=24.59
# Case 4, Moves=26, Opened=13911166, Time=81.77
# Case 5, Moves=18, Opened=116780, Time=0.66
# Case 6, Moves=20, Opened=416138, Time=2.40
# Case 7, Moves=14, Opened=11775, Time=0.07
# Case 8, Moves=24, Opened=2892380, Time=16.66
# Case 9, Moves=22, Opened=950220, Time=5.43
# Case 10, Moves=31, Opened=134346370, Time=791.46

import time
from copy import deepcopy

MAX_DEPTH = 31
TEST_CASES = {
    1: {'start_state': [0, 0, [[0, 7, 1], [4, 3, 2], [8, 6, 5]]], 'goal_state': [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]},
    2: {'start_state': [0, 2, [[5, 6, 0], [1, 3, 8], [4, 7, 2]]], 'goal_state': [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]},
    3: {'start_state': [2, 0, [[3, 5, 6], [1, 2, 7], [0, 8, 4]]], 'goal_state': [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]},
    4: {'start_state': [1, 1, [[7, 3, 5], [4, 0, 2], [8, 1, 6]]], 'goal_state': [0, 2, [[3, 2, 0], [6, 1, 8], [4, 7, 5]]]},
    5: {'start_state': [2, 0, [[6, 4, 8], [7, 1, 3], [0, 2, 5]]], 'goal_state': [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]},
    6: {'start_state': [0, 0, [[0, 1, 8], [3, 6, 7], [5, 4, 2]]], 'goal_state': [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]},
    7: {'start_state': [2, 0, [[6, 4, 1], [7, 3, 2], [0, 5, 8]]], 'goal_state': [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]},
    8: {'start_state': [0, 0, [[0, 7, 1], [5, 4, 8], [6, 2, 3]]], 'goal_state': [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]},
    9: {'start_state': [0, 2, [[5, 4, 0], [2, 3, 1], [8, 7, 6]]], 'goal_state': [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]},
    10: {'start_state': [2, 1, [[8, 6, 7], [2, 5, 4], [3, 0, 1]]], 'goal_state': [2, 2, [[1, 2, 3], [4, 5, 6], [7, 8, 0]]]},
}

nodes_opened = 0

def get_possible_moves(state):
    DIRECTIONS = [(1, 0), (-1, 0), (0, -1), (0, 1)]  # Down, Up, Left, Right
    
    # Separate the state into x, y, and the grid
    x, y, grid = state
    
    # Iterate over all possible directions
    for dx, dy in DIRECTIONS:
        # Calculate the new x and y coordinates
        nx, ny = x + dx, y + dy
        
        # Check if within grid
        if 0 <= nx < len(grid) and 0 <= ny < len(grid[0]):
            new_grid = deepcopy(grid)
            
            # Swap the blank tile with the new tile
            new_grid[x][y], new_grid[nx][ny] = new_grid[nx][ny], new_grid[x][y]
            
            yield [nx, ny, new_grid]


def dfs_generator(state, goal, depth, path):
    global nodes_opened
    nodes_opened += 1
    
    # If the current state is the goal state, return the path
    if state == goal:
        yield path
        return
    
    # Finish if the depth is 0
    if depth == 0:
        return
    
    for move in get_possible_moves(state):
        # Avoid going back to the previous state
        if move in path:
            continue
        
        # Recursively call the generator for the next state
        yield from dfs_generator(move, goal, depth - 1, path + [move])


def iddfs(start_state, goal_state):
    global nodes_opened
    nodes_opened = 0
    depth = 0
    start_time = time.time()
    
    while True:
        # Call the DFS generator
        for result in dfs_generator(start_state, goal_state, depth, [start_state]):
            return len(result) - 1, nodes_opened, time.time() - start_time
        
        # Increase the depth and try again
        depth += 1
        
        # If the depth exceeds the maximum depth, return None
        if depth > MAX_DEPTH:
            return None, nodes_opened, time.time() - start_time


def solve_puzzle(start_state, goal_state):
    moves, nodes_opened, elapsed_time = iddfs(start_state, goal_state)
    return moves, nodes_opened, elapsed_time


def main():
    for i, test_case in TEST_CASES.items():
        start_state = test_case['start_state']
        goal_state = test_case['goal_state']
        moves, nodes_opened, elapsed_time = solve_puzzle(start_state, goal_state)
        print(f'Case {i}, Moves={moves}, Opened={nodes_opened}, Time={elapsed_time:.2f}')


if __name__ == '__main__':
    main()