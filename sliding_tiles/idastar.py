# Case 1, Moves=18, Opened=246, Time=0.00
# Case 2, Moves=22, Opened=2707, Time=0.03
# Case 3, Moves=24, Opened=5759, Time=0.06
# Case 4, Moves=26, Opened=16435, Time=0.17
# Case 5, Moves=18, Opened=213, Time=0.00
# Case 6, Moves=20, Opened=132, Time=0.00
# Case 7, Moves=14, Opened=36, Time=0.00
# Case 8, Moves=24, Opened=1892, Time=0.02
# Case 9, Moves=22, Opened=2609, Time=0.03
# Case 10, Moves=31, Opened=22801, Time=0.24

import time
from copy import deepcopy

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


def manhattan_distance(start_state, goal_state):
    # Separate the start and goal states into x, y, and the grid
    _, _, start_grid = start_state
    _, _, goal_grid = goal_state
    
    # Create a dictionary to store the coordinates of each number in the goal state
    goal_positions = {}
    for i, row in enumerate(goal_grid):
        for j, num in enumerate(row):
            goal_positions[num] = (i, j)
    
    # Calculate the Manhattan distance
    distance = 0
    for i, row in enumerate(start_grid):
        for j, num in enumerate(row):
            if num != 0:
                gi, gj = goal_positions[num]
                distance += abs(i - gi) + abs(j - gj)
    
    return distance


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


def ida_star_recursive(current_state, current_cost, cost_bound, current_path, target_state, visited_states, nodes_expanded):
    # Calculate the estimated cost
    estimated_cost = current_cost + manhattan_distance(current_state, target_state)
    
    if estimated_cost > cost_bound:
        yield estimated_cost, None  
        return
    
    if current_state == target_state:
        yield True, current_path 
        return
    
    minimum_exceeding_cost = float('inf')

    # Loop through all possible moves
    for move in get_possible_moves(current_state):
        move_state_tuple = tuple(map(tuple, move[2]))
        
        # Ignore visited states
        if move_state_tuple in visited_states:
            continue
        
        visited_states.add(move_state_tuple)
        nodes_expanded[0] += 1
        
        # Recursively call the generator for the next state
        recursive = ida_star_recursive(move, current_cost + 1, cost_bound, current_path + [move], target_state, visited_states, nodes_expanded)
        
        for result, new_path in recursive:
            # If the goal state is reached, return the path
            if result is True:
                yield True, new_path
                return
        
            # Update the minimum cost
            if isinstance(result, (int, float)):
                minimum_exceeding_cost = min(minimum_exceeding_cost, result)
            yield result, new_path
        
        # Remove the visited state
        visited_states.remove(move_state_tuple)
    
    yield minimum_exceeding_cost, None


def solve_puzzle(start_state, goal_state):
    start_time = time.time()
    bound = manhattan_distance(start_state, goal_state)
    nodes_opened = [0]
    
    while True:
        visited = {tuple(map(tuple, start_state[2]))}
        generator = ida_star_recursive(start_state, 0, bound, [start_state], goal_state, visited, nodes_opened)
        
        min_cost = float('inf')
        for result, path in generator:
            # If the goal state is reached, return the path
            if result is True:
                return len(path) - 1, nodes_opened[0], time.time() - start_time, path
            
            # Update the minimum cost
            if isinstance(result, (int, float)):
                min_cost = min(min_cost, result)
        
        # If the minimum cost is infinity, return None
        if min_cost == float('inf'):
            return None, nodes_opened[0], time.time() - start_time, None
        
        # Update the cost bound
        bound = min_cost


def main():
    for i, test_case in TEST_CASES.items():
        start_state = test_case['start_state']
        goal_state = test_case['goal_state']
        moves, nodes_opened, elapsed_time, path = solve_puzzle(start_state, goal_state)
        print(f'Case {i}, Moves={moves}, Opened={nodes_opened}, Time={elapsed_time:.2f}')


if __name__ == '__main__':
    main()
