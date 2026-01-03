import random
from itertools import permutations
import heapq

def generate_states(n, print_states=False):
    """
    Input: n representing rows and comums for nxn square game
    returns: all possible states of nxn square
    SOLVES PART A
    """
    state_0 = {i for i in range(n**2)}
    state_0_list = list(state_0)
    states = []
    #generate all 362,000 states as a list
    for p in permutations(state_0_list):
        states.append(p)
    
    if(print_states):
        print(states)
    return states

def oddneighborcheck(state):
    """
    Input: flattned 1d array representing 2D 3x3 array
    Output: True if no value is odd and has an odd neighbor
    """
    n = int(len(state)**.5)
            
    for i, val in enumerate(state) :
        if val % 2 != 0:
            #check up
            if 0 <= i-n < len(state) and (state[i-n] % 2 != 0):
                return False
            #check down
            if 0 <= i+n < len(state) and (state[i+n] % 2 != 0): 
                return False
            #check left
            if i%n != 0 and (state[i-1] % 2 != 0): 
                return False
            #check right
            if (i+1)%n != 0 and (state[i+1] % 2 != 0): 
                return False
    return True
        
            

def get10States(states):
    """
    input: list of all states.
    output: 10 randomly selected states must not have odd numbered neighbors
    SOLVES PART B
    """
    chosen_10 = []
    while len(chosen_10) != 10:
        chosen_state = random.choice(states)
        if oddneighborcheck(chosen_state):
            chosen_10.append(chosen_state)
            states.remove(chosen_state)
    return chosen_10

def puzzle_move(state, action):
    """
    Input: 1d array representing a state and an action (up, down, left, right)
    output: next state
    show resulting state after moving blank piece
    SOLVES PART C
    """
    ### you can also represent all the states as a graph
    n = int(len(state)**.5)
    idx = state.index(0)
    new_state = state.copy()

    if 0 <= idx-n < len(state) and (state[idx-n] % 2 != 0) and action == 1:
        #return the new state  
        #up
        new_state[idx] = state[idx-n]
        new_state[idx-n] = 0
    #check down
    elif 0 <= idx+n < len(state) and (state[idx+n] % 2 != 0) and action == 2: 
        new_state[idx] = state[idx+n]
        new_state[idx+n] = 0
    #check left
    elif idx%n != 0 and (state[idx-1] % 2 != 0) and action == 3: 
        new_state[idx] = state[idx-1]
        new_state[idx-1] = 0
    #check right
    elif (idx+1)%n != 0 and (state[idx+1] % 2 != 0) and action == 4: 
        new_state[idx] = state[idx+1]
        new_state[idx+1] = 0
    else:
        #print("invalid input")
        return state

    return new_state


def puzzle_move_2(state, action):
    """
    Input: 1d array representing a state and an action (up, down, left, right)
    output: next state
    show resulting state after moving blank piece
    SOLVES PART C
    """
    ### you can also represent all the states as a graph
    n = int(len(state)**.5)
    idx = state.index(0)
    new_state = state.copy()

    if 0 <= idx-n < len(state) and action == 1:
        #return the new state  
        new_state[idx] = state[idx-n]
        new_state[idx-n] = 0
    #check down
    elif 0 <= idx+n < len(state)  and action == 2: 
        new_state[idx] = state[idx+n]
        new_state[idx+n] = 0
    #check left
    elif idx%n != 0 and action == 3: 
        new_state[idx] = state[idx-1]
        new_state[idx-1] = 0
    #check right
    elif (idx+1)%n != 0 and action == 4: 
        new_state[idx] = state[idx+1]
        new_state[idx+1] = 0
    else:
        #print("invalid input")
        return state

    return new_state

def rand_div_3(state):
    """
    Input: 1d array representing nxn grid
    SOLVES part D
    """
    # calculate size of grid
    n = int(len(state)**.5)
    #initialize solved bool, step count, path
    solved = False
    steps = 0
    path = [state]
    while not solved:
        solved = True
        # for each row of grid
        for i in range(n):
            #check if a row is divisible by 3
            total = (100*state[i*n]) + (10*state[(i*n) + 1]) + (1*state[(i*n) + 2]) 
            if total % 3 != 0:
                #update vars and break if a row is not divisible by 3
                solved = False
                state = puzzle_move(state, random.randint(1, 4))
                steps += 1
                path.append(state)
                break
    return state, steps, path

def bfs_solve(start_state):
    """
    Input: start state
    SOLVE PART E
    """
    #add start to queue and visited
    queue = [(start_state, [], [start_state])]
    visited = {tuple(start_state)}

    #while queue isn't empty
    while queue:
        #deque state
        state, actions, state_seq = queue.pop(0)
        #if state is goal return state and path
        if state == [0,1,2,3,4,5,6,7,8]:
            return state, actions, state_seq
        #check each possible path 
        for action in [1,2,3,4]:
            next_state = puzzle_move_2(state, action)
            #if next state isnt visited
            if tuple(next_state) not in visited:
                #mark next state as visited and add to queue
                visited.add(tuple(next_state))
                queue.append((next_state, actions + [action], state_seq + [next_state]))
    return None


def dfs_solve(start_state):

    """
    I couldn't print the list of states becuase it crashed my computer
    THe output list of actions is too long so I couldnt print it
    Input: start_State: list
    SOLVE PART F
    """
    #initialize stack and visited set
    stack = [(start_state, [])]  
    visited = set()
    # while stack isn't empty
    while stack:
        #pop state
        state, actions = stack.pop()
        #if its been visited go to next iteration
        if tuple(state) in visited:
            continue
        #add state to visited
        visited.add(tuple(state))
        #if its the goal return
        if state == [0,1,2,3,4,5,6,7,8]:
            return state, actions
        #check child states
        for action in [1, 2, 3, 4]:
            next_state = puzzle_move_2(state, action)
            if next_state != state:
                stack.append((next_state, actions + [action]))

    return None

def partG(start_state):
    """
    Input: start state
    SOLVE PART G
    """
    #add start to queue and visited
    queue = [(start_state, [], [start_state])]
    visited = {tuple(start_state)}

    #while queue isn't empty
    while queue:
        #deque state
        state, actions, state_seq = queue.pop(0)
        #if state is goal return state and path
        if state == [1,2,3,8,0,4,7,6,5]:
            return state, actions, state_seq
        #check each possible path 
        for action in [1,2,3,4]:
            next_state = puzzle_move_2(state, action)
            #if next state isnt visited
            if tuple(next_state) not in visited:
                #mark next state as visited and add to queue
                visited.add(tuple(next_state))
                queue.append((next_state, actions + [action], state_seq + [next_state]))
    return None


def ucs_solve(start_state):
    #prio queue and set
    prio_queue = []
    visited = set()
    #push info to prio queue
    heapq.heappush(prio_queue, (0,start_state, [], []))
    #while not empty
    while prio_queue:
        #pop values from prio queue
        cost, state, path, state_seq  = heapq.heappop(prio_queue)
        #go to next iteration if visited
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        #if goal rturn
        if state == [0,1,2,3,4,5,6,7,8]:
            return cost, state, path, state_seq
        # check child nodes
        for action in [1,2,3,4]:
            next_state = puzzle_move_2(state, action)
            if next_state != state:
                heapq.heappush(prio_queue, ( cost+1, next_state, path + [action], state_seq + [tuple(next_state)]))
    return None

def ucs_solve_2(start_state):
    #prio queue and set
    prio_queue = []
    visited = set()
    #push info to prio queue
    heapq.heappush(prio_queue, (0,start_state, [], []))
    #while not empty
    while prio_queue:
        #pop values from prio queue
        cost, state, path, state_seq  = heapq.heappop(prio_queue)
        #go to next iteration if visited
        if tuple(state) in visited:
            continue
        visited.add(tuple(state))
        #if goal rturn
        if state == [0,1,2,3,4,5,6,7,8]:
            return cost, state, path, state_seq
        # check child nodes
        for action in [1,2,3,4]:
            next_state = puzzle_move_2(state, action)
            if next_state != state:
                if action == 1:
                    heapq.heappush(prio_queue, ( cost+1.5, next_state, path + [action], state_seq + [tuple(next_state)]))
                if action == 2:
                    heapq.heappush(prio_queue, ( cost+.5, next_state, path + [action], state_seq + [tuple(next_state)]))
                if action == 3:
                    heapq.heappush(prio_queue, ( cost+1, next_state, path + [action], state_seq + [tuple(next_state)]))
                if action == 4:
                    heapq.heappush(prio_queue, ( cost+2, next_state, path + [action], state_seq + [tuple(next_state)]))
    return None


def main(): 
    print("Part A & B")
    states = generate_states(3) #SOLVE PART A BY GENERATING ALL POSSIBLE STATES
    #states = generate_states(3, True)
    print(get10States(states)) #SOLVE PART B BY PRINTING 10 RANDOM STATES WITH NO ODD NEIGHBORS
    print("\nPart C")
    print(int(''.join(map(str,puzzle_move([7,2,4,5,0,6,8,3,1], 3))))) #SOLVE PART c BY MOVING PUZZLE PIECE
    print("\nPart D")
    state, steps, path = rand_div_3([7,2,4,5,0,6,8,3,1])
    print(f"Final state: {state}\n Number of steps: {steps}\n Path: {path}") #SOLVE PART D BY ARRANGING ARRAY SUCH THAT IT MUST BE DIVISIBLE BY 3
    print("\nPart E")
    state, actions, state_seq = bfs_solve([4,0,2,1,3,7,6,8,5])
    print(f"state: {state} \n states: {state_seq} \n len_path: {len(actions)}") 
    print("\nPart F")
    state, actions = dfs_solve([4,0,2,1,3,7,6,8,5])
    print(f"state: {state}, len_path: {len(actions)}")
    print("\nPart G")
    state, actions, state_seq = partG([8,1,2,7,0,3,6,4,5])
    print(f"state: {state}, len_path: {len(actions)}")

    print("\nPart H-A: Uniform Cost")
    cost, state, actions, state_seq = ucs_solve([4,0,2,1,3,7,6,8,5])
    print(f"state: {state}\n state_sequence: {state_seq}\n action_seq: {actions} \n")

    print("\nPart H-B: Uniform Cost")
    cost, state, actions, state_seq = ucs_solve_2([4,0,2,1,3,7,6,8,5])
    print(f"state: {state}\n state_sequence: {state_seq}\n action_seq: {actions} \n")


if __name__ == "__main__":
    main()





