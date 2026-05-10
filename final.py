import heapq
import sys
import random
import time
from turtle import pd

sys.setrecursionlimit(10**4)

def empty(state):
    """Finds the position of the empty cell and returns its coordinates."""

    for i in range(len(state)):
        for j in range(len(state)):
            if state[i][j] == 0:
                return(i, j)
            
def children(state):
    """Returns an array of all possible moves from a given state."""
    
    zero = empty(state)
    moves = []

    if zero[0]>0: # zero goes up
        move = [list(i) for i in state].copy()
        temp = move[zero[0]-1][zero[1]]
        move[zero[0]-1][zero[1]] = move[zero[0]][zero[1]]
        move[zero[0]][zero[1]] = temp
        moves.append([tuple(i) for i in move])
               
    if zero[1]>0: #left
        move = [list(i) for i in state].copy()
        temp = move[zero[0]][zero[1]-1]
        move[zero[0]][zero[1]-1] = move[zero[0]][zero[1]]
        move[zero[0]][zero[1]] = temp
        moves.append([tuple(i) for i in move])
    
    if zero[1]<len(state)-1: #right
        move = [list(i) for i in state].copy()
        temp = move[zero[0]][zero[1]+1]
        move[zero[0]][zero[1]+1] = move[zero[0]][zero[1]]
        move[zero[0]][zero[1]] = temp
        moves.append([tuple(i) for i in move])
    
    if zero[0]<len(state)-1: #down 
        move = [list(i) for i in state].copy()
        temp = move[zero[0]+1][zero[1]]
        move[zero[0]+1][zero[1]] = move[zero[0]][zero[1]]
        move[zero[0]][zero[1]] = temp
        moves.append([tuple(i) for i in move])

    return moves

def read_data(nums):
    N = int(len(nums) ** 0.5)
    data = []

    if len(nums) != N*N:
        print('incorrect input')
        return

    for i in range(0, len(nums), N):
        row = tuple(nums[i:i+N])
        data.append(row)

    return data

def goal_test(state, target):
    """Checks whether the current state is the goal state."""

    return 1 if state == target else 0

def show_path(path_data, node, start):
    """Returns a path from the start state to the target state recursively."""

    if node == start:
        return [node]
        
    result = show_path(path_data, path_data[tuple(node)], start)
    result.append(node)
    return result

def pos_in_target(point, target):
    """Finds the position of a tile in the target state and returns its coordinates."""

    for i in range(len(target)):
        for j in range(len(target)):
            if target[i][j] == point:
                return i, j

def queueing_function(state, target, halgo):
    """
    For given state, calculates the value of the queueing function.

    halgo defines the algorithm type: 1 is Uniform, 2 is Manhattan heuristic, 3 is misplaced tiles heuristic.
    """
    
    dist = 0

    if halgo == 1: # 1 is Uniform
        return dist 
        
    for i in range(len(state)):
        for j in range(len(state)):

            if state[i][j] == 0:
                continue

            if halgo == 2: # 2 is Manhattan
                dist += abs(i - pos_in_target(state[i][j], target)[0]) + abs(j - pos_in_target(state[i][j], target)[1])

            else: # misplaced
                if state[i][j] != target[i][j]:
                    dist += 1

    return dist

def A_star_search(start, target, halgo=1):
    """
    The general search function. The halgo parameter denotes the algorithm type.
    """

    path_data = {}
    queue = []
    used = [] # used nodes
    g, exposed = 0, 0 # g is the cost and exposed is the number of exposed nodes
    
    # heapq helps to get the cheapest node from the queue
    heapq.heappush(queue, [g + queueing_function(start, target, halgo), g, start]) # f = g+h

    memory_usage = 1 # the maximum number of nodes in the queue at a specific time step.
    
    while queue:
        f, g, node = heapq.heappop(queue)
    
        if goal_test(node, target):
            # If it is the goal state, then the task is solved.

            print('The level of the target state: ', g)
            break
    
        if node in used:
            continue

        exposed += 1
        for child in children(node):
            if child not in used:
                
                # Update f and g values:
                g_child = g + 1 # increase at each level
                f_child = g_child + queueing_function(child, target, halgo)
                
                # Add the child node to the queue.
                heapq.heappush(queue, [f_child, g_child, child])
    
                path_data[tuple(child)] = node
                
        used.append(node)

        # As we need to estimate the memory usage, we save the maximum value between these two:
        memory_usage = max(len(queue), memory_usage) 

    path = show_path(path_data, target, start)
    return (g, exposed, memory_usage, path, len(path))

def test_states(state, n_moves):
    """Takes the target state and a number of moves to make from it, 
    and returns a state that is n_moves away from the target state, thus providing a valid start state.
    """
    last_position = state # save last position to avoid getting back.

    for i in range(n_moves):
        all_moves = children(state)

        next_moves = []

        for move in all_moves:
            if move != last_position:
                next_moves.append(move)

        last_position = state
        state = random.choice(next_moves)

    return state

def create_target(n):
    """Creates target in case a user decides to generate start state rather than to impute it."""
    x = list(range(1, n * n))
    x.append(0)
    return read_data(x)

def ask_user():
    """User's input."""

    n = int(input('Please enter the puzzle size (number of rows on the board): '))
    print('\nEnte ', n * n, ' numbers from 0 to', n * n - 1, ' with spaces.')
    x = input(' ').split()
    x = [int(i) for i in x]
    start = read_data(x)
    target = create_target(n)

    return start, target

def get_generated_state():
    """If users chooses to generate start state."""

    n = int(input('Please enter the puzzle size (number of rows on the board): '))
    n_moves = int(input("\nEnter the number of random moves: "))

    target = create_target(n)
    start = test_states(target, n_moves)

    return start, target

def run_experiments(start, target):
    """Runs the three algorithms and returns the results."""
    results = []

    for algo_type in range(1, 4):

        if algo_type == 1:
            algo_name = 'Uniform Search'
        elif algo_type == 2:
            algo_name = 'A* with Manhattan heuristic'
        else:
            algo_name = 'A* with misplaced tiles heuristic'

        print('\n\n', algo_name)

        start_time = time.perf_counter()
        g, exposed, memory_usage, path, path_length = A_star_search(start, target, algo_type)
        execution_time = time.perf_counter() - start_time

        print('Target level:', g)
        print('Exposed nodes:', exposed)
        print('Max number of values in the queue:', memory_usage)
        print('Path length:', path_length)
        print('Time:', execution_time)


if __name__ == "__main__":

    print('Enter 1 to enter start state manually or 2 to generate it randomly: ')
    choice = input("")

    if choice == "1":
        start, target = ask_user()
    elif choice == "2":
        start, target = get_generated_state()

    print('\n\nStart state: ')
    for i in start:
        print(i)

    print('\nTarget state:')
    for i in target:
        print(i)

    run_experiments(start, target)
