### Programming Assignment 2: Markov Decision Processes
### CPSC 4420
### Kevius Tribble
import argparse

### represent MDP as a class
class MDPenv:
    ### will need to store grid size, terminal states, walls, obstacles,actions & values, all states (x,y, direction of robot)
    def __init__(self, grid_size, terminal_states, walls, obstacles):
        self.grid_size = grid_size #interger for nxn grid
        self.terminal_states = terminal_states #dictionary of terminal states and their reward
        self.walls = walls # dictionarry with cell as key and blocked cells as list of tuples
        self.states = [] # list of all states (x,y,d)
        self.actions = {1: -1.0, 2: -1.5, 3:-0.5, 4:-0.5} #foward 1 cell, forward 2 cell, turn left, turn right
        self.obstacles = obstacles # set of (x,y) pairs representing blocked cells

        ### populate list of states
        for x in range(1, self.grid_size+1):
            for y in range(1, self.grid_size+1):
                if (x,y) not in obstacles:
                    for dir in range(1,5):
                        self.states.append((x,y,dir)) # 1 = up, 2 = right, 3 = down, 4 = left

    def is_state_valid(self, state):
        x,y,d = state
        #check bounds
        if x < 1 or x > self.grid_size or y < 1 or y > self.grid_size:
            return False
        #check for obstacle
        if (x,y) in self.obstacles:
            return False
        #check walls
        if (x,y) in self.walls:
            for wall in self.walls[(x,y)]:
                if d == 1 and wall == (x, y+1): #facing up check
                    return False
                if d == 2 and wall == (x+1,y): #face right check
                    return False
                if d == 3 and wall == (x, y-1): # face down check
                    return False
                if d == 4 and wall == (x-1, y): #face left check
                    return False
        return True
    
    
    def transition(self, state, action):
        x,y,d = state
        if (x,y) in self.terminal_states:
            return state, 0
        if action == 1: # move forward 1
            if d == 1:
                next_state = (x, y+1, d)
            if d == 2:
                next_state = (x+1, y, d)
            if d == 3:
                next_state = (x, y-1, d)
            if d == 4:
                next_state = (x-1, y, d)
        elif action == 2: #move forward 2
            if d == 1:
                next_state_inter = (x, y+1, d)
                next_state = (x, y+2, d)
            if d == 2:
                next_state_inter = (x, y+1, d)
                next_state = (x+2, y, d)
            if d == 3:
                next_state_inter = (x, y+1, d)
                next_state = (x, y-2, d)
            if d == 4:
                next_state_inter = (x, y+1, d)
                next_state = (x-2, y, d)
        elif action == 3: # turn right
            next_state = (x,y, (d%4)+1)
        elif action == 4: # turn left
            next_state = (x,y, (d-2)%4+1)

        #calculate reward 
        reward = self.actions[action]
        x_next, y_next, d_next= next_state
        # check intermediate state for action 2 incase of walls/obstacles
        if action == 2:
            x_inter, y_inter, d_inter = next_state_inter
            if not self.is_state_valid(next_state_inter):
                return state, reward
        if self.is_state_valid(next_state):
            if (x_next,y_next) in self.terminal_states:
                reward += self.terminal_states[(x_next,y_next)]
            return next_state, reward
        else:
            return state, reward
                    
### make a function that uses the MDP_ENV class to do value iteration
def value_iteration(MDPenv, gamma, noise, iterations, print_data=True):
    # gamma = reward decay
    # noise = probability of incorrect action 
    v = {s: 0 for s in  MDPenv.states}
    policy = {s: 0 for s in MDPenv.states}
    full_policy = [list() for i in range(iterations)]
    actions = list(MDPenv.actions.keys())
    #for each iteration calculate the Optimal value for each state
    for i in range(iterations):
        v_new = v.copy()
        for state in MDPenv.states:
            #value iteration calculation
            # 1. find probability of action 
            action_values = {}
            for action in actions:
                #get the correct probabilities
                p_desired = 1 - noise
                p_other = noise/(len(actions)-1)
                expected_value = 0
                for a in actions:
                    if a == action:
                        p = p_desired
                    else: 
                        p = p_other
                    # 2. get reward and next state using transition model
                    next_state, reward = MDPenv.transition(state, action)
                    # 3. calculate exptected value
                    expected_value += (p*(reward + gamma*v[(next_state)]))#calculate expected value
                action_values[action] = expected_value 
            #retrieve the policy
            best_action = max(action_values, key=action_values.get)
            v_new[state] = action_values[best_action]

            policy[state] = best_action
            #print first 10 iterations
            if print_data:
                if (i < 10):
                    for state in sorted(MDPenv.states):
                        print(f"iteration {i+1}: ")
                        print(f"State: {state}, Value: {v[state]:.2f}, Best Action: {policy[state]}")
        full_policy[i] = policy
        v=v_new
    return full_policy #returns final V, policy, a full policy list

#write a function to follow the optinal policy. Will need to output the policies for all iterations. 
def optimal_path(start, stop, policy):
    grid_size = 5
    obstacles = {(2,5), (3,2), (4,5)} 
    walls = {(1,4):[(1,3)], \
                      (1,3): [(1,2), (1,4)], \
                      (5,4):[(5,3)], \
                      (5,3): [(5,2), (5,4)],\
                      (1,2):[(1,3)], \
                      (5,2):[(5,3)] \
                      }
    terminal_states = {(5,5): 100, (3,4): -1000}
    mdp = MDPenv(grid_size, terminal_states, walls, obstacles)
    curr_state = start
    states = []
    for i in range(10): #limit to 10 steps
        states.append(curr_state)
        if i < len(policy) and curr_state in policy[i]:
            next_state, reward = mdp.transition(curr_state, policy[i][curr_state])
            curr_state = next_state
            # stop when goal is reached
            if curr_state[0:2] == stop[0:2]:
                states.append(curr_state)
                break
    return states

def main(argv=None, **kwargs):
    ### command line args to pick between parts B-F
    parser = argparse.ArgumentParser(description="MDP Value Iteration")
    parser.add_argument('--part', type=str, choices=['B', 'C', 'D', 'E', 'F'], required=True, help="Part of the assignment to run (B, C, D, E, F)")
    args = parser.parse_args()

    #define mdp paraqmeters
    grid_size = 5
    obstacles = {(2,5), (3,2), (4,5)} 
    walls = {(1,4):[(1,3)], \
                      (1,3): [(1,2), (1,4)], \
                      (5,4):[(5,3)], \
                      (5,3): [(5,2), (5,4)],\
                      (1,2):[(1,3)], \
                      (5,2):[(5,3)] \
                      }
    terminal_states = {(5,5): 100, (3,4): -1000}

    mdp = MDPenv(grid_size, terminal_states, walls, obstacles)

    #part B
    if args.part == 'B':
        full_policy = value_iteration(mdp, gamma=1, noise=0, iterations=100)
    #part c = follow the policy
    if args.part == 'C':
        full_policy = value_iteration(mdp, gamma=1, noise=0, iterations=100)
        print(optimal_path((1,1,1), (5,5,1), full_policy))
    #part D = gamma = .9
    if args.part == 'D':
        full_policy = value_iteration(mdp, gamma=.9, noise=0, iterations=100)
        print(optimal_path((1,1,1), (5,5,1), full_policy))
    #part E gamma = .1
    if args.part == 'E':
        full_policy = value_iteration(mdp, gamma=.1, noise=0, iterations=100)
        print(optimal_path((1,1,1), (5,5,1), full_policy))
    #part F gamma = .9 & noise = .1
    if args.part == 'F':
        full_policy = value_iteration(mdp, gamma=.9, noise=.1, iterations=100)
        print(optimal_path((1,1,1), (5,5,1), full_policy))

if __name__ == "__main__":
    main()
