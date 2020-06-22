"""
Skeleton code for Project 1 of Columbia University's AI EdX course (8-puzzle).
Python 3
"""

import queue as Q

import time

import sys

if sys.platform == "win32":
    import psutil
    print("psutil", psutil.Process().memory_info().rss)
else:
    # Note: if you execute Python from cygwin,
    # the sys.platform is "cygwin"
    # the grading system's sys.platform is "linux2"
    import resource
    print("resource", resource.getrusage(resource.RUSAGE_SELF).ru_maxrss)

import math

#### SKELETON CODE ####

## The Class that Represents the Puzzle

class PuzzleState(object):

    """docstring for PuzzleState"""

    def __init__(self, config, n, parent=None, action="Initial", cost=0,maxDepth = 0):

        if n*n != len(config) or n < 2:

            raise Exception("the length of config is not correct!")

        self.n = n

        self.cost = cost

        self.parent = parent

        self.action = action

        self.dimension = n

        self.config = config

        self.children = []
        self.maxDepth = maxDepth

        for i, item in enumerate(self.config):

            if item == 0:

                self.blank_row = i // self.n

                self.blank_col = i % self.n

                break

    def display(self):

        for i in range(self.n):

            line = []

            offset = i * self.n

            for j in range(self.n):

                line.append(self.config[offset + j])

            print(line)

    def move_left(self):

        if self.blank_col == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]
            return PuzzleState(tuple(new_config), self.n, parent=self, action="Left", cost=self.cost + 1,maxDepth = self.maxDepth+1)

    def move_right(self):

        if self.blank_col == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + 1

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Right", cost=self.cost + 1,maxDepth = self.maxDepth+1)

    def move_up(self):

        if self.blank_row == 0:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index - self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Up", cost=self.cost + 1,maxDepth = self.maxDepth+1)

    def move_down(self):

        if self.blank_row == self.n - 1:

            return None

        else:

            blank_index = self.blank_row * self.n + self.blank_col

            target = blank_index + self.n

            new_config = list(self.config)

            new_config[blank_index], new_config[target] = new_config[target], new_config[blank_index]

            return PuzzleState(tuple(new_config), self.n, parent=self, action="Down", cost=self.cost + 1,maxDepth = self.maxDepth+1)

    def expand(self):

        """expand the node"""

        # add child nodes in order of UDLR

        if len(self.children) == 0:

            up_child = self.move_up()

            if up_child is not None:
               
                self.children.append(up_child)

            down_child = self.move_down()

            if down_child is not None:
    
                self.children.append(down_child)

            left_child = self.move_left()

            if left_child is not None:
                
                self.children.append(left_child)

            right_child = self.move_right()

            if right_child is not None:
                self.children.append(right_child)

        return self.children
    
    def printPath(self, path= []):
        # if( self.action != "Initial" ):
        #     self.parent.printPath(path)
        # path.append(self.action)
        s = Q.LifoQueue()
        currentState = self
        while currentState.parent != None:
            s.put(currentState)
            currentState = currentState.parent
        while not s.empty():
            path.append(s.get().action)
            
        

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters

def writeOutput(method,initial_state,goalPath,Cost, nodeExpand, searchDepth, maxDepth):

    ### Student Code Goes here
    print("output")
    outputFile = open('output.txt','a')
    outputFile.write(method)
    outputFile.write(' '.join(str(s) for s in initial_state.config))
    outputFile.write("\nGoal Path: ")
    outputFile.write(' '.join(str(s) for s in goalPath))
    outputFile.write("\nCost: ")
    outputFile.write(str(Cost))
    outputFile.write("\nNode Expand: ")
    outputFile.write(str(nodeExpand))
    outputFile.write("\nSearch Depth: ")
    outputFile.write(str(searchDepth))
    outputFile.write("\nMax Depth: ")
    outputFile.write(str(maxDepth))
    outputFile.write("\n\n***************\n\n")
    outputFile.close()
     

def bfs_search(initial_state):
    
    """BFS search"""
    t0 = time.time()
    # print("Initial State:")
    # print(initial_state.display())
    q = Q.Queue()
    q.put(initial_state)
    q.put(None)
    visited = set()
    goalPath = []
    visited.add(initial_state.config)
    maxDepth = 1
    nodesExpand = 0
    while not q.empty():
        currentState = q.get();
        if(currentState == None):
            maxDepth += 1
            q.put(None)
            continue
        if test_goal(currentState):
                # print("State Found")
                # print(currentState.display())
                currentState.printPath(goalPath)
                writeOutput("BFS ",initial_state,goalPath,currentState.cost,nodesExpand,len(goalPath),maxDepth)
                break
        currentState.expand();
        nodesExpand += 1
        children = list(currentState.children)
        for item in children:
            if( (item.config not in visited) ):
                q.put(item)
                visited.add(item.config)
    t1 = time.time()
    print('BFS takes: {} sec'.format(t1-t0))
            
    ### STUDENT CODE GOES HERE ###

def dfs_search(initial_state):

    """DFS search"""
    t0 = time.time()
    s = Q.LifoQueue()
    
    visited = set()
    visited.add(initial_state.config)
    nodesExpand  = 0
    goalPath = []
    # s.put(None)
    s.put(initial_state)
    maxDepth = 1
    print("ok")
    while not s.empty():
        currentState = s.get()
        if test_goal(currentState):
            currentState.printPath(goalPath)
            writeOutput("DFS ",initial_state, goalPath, currentState.cost, nodesExpand, len(goalPath), maxDepth)
            break
        currentState.expand()
        nodesExpand += 1
        children = currentState.children
        for i in range(len(children), 0,-1):
            if children[i-1].config not in visited:
                s.put(children[i-1])
                maxDepth = max(maxDepth, children[i-1].maxDepth)
                visited.add(children[i-1].config)
    t1 = time.time()
    print("DFS: {}".format(t1-t0))
                
        
    ### STUDENT CODE GOES HERE ###

def A_star_search(initial_state):

    """A * search"""
    print("astar")
    ### STUDENT CODE GOES HERE ###

def calculate_total_cost(state):

    """calculate the total estimated cost of a state"""

    ### STUDENT CODE GOES HERE ###

def calculate_manhattan_dist(idx, value, n):

    """calculate the manhattan distance of a tile"""

    ### STUDENT CODE GOES HERE ###

def test_goal(puzzle_state):
    dimension = puzzle_state.dimension
    goalconfig = tuple(range(0, dimension*dimension))
    if(puzzle_state.config == goalconfig):
        return True
    else:
        return False
    """test the state is the goal state or not"""
    
    ### STUDENT CODE GOES HERE ###

# Main Function that reads in Input and Runs corresponding Algorithm

def main():

    sm = sys.argv[1].lower()

    begin_state = sys.argv[2].split(",")

    begin_state = tuple(map(int, begin_state))

    size = int(math.sqrt(len(begin_state)))

    hard_state = PuzzleState(begin_state, size)

    if sm == "bfs":

        bfs_search(hard_state)

    elif sm == "dfs":

        dfs_search(hard_state)

    elif sm == "ast":

        A_star_search(hard_state)

    else:

        print("Enter valid command arguments !")

if __name__ == '__main__':

    main()