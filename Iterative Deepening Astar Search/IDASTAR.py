import random                                   #Import random for generating random values
import math                                     #Import math for finding square root
import time                                     #Import time for finding process time span
import psutil                                   #Import psutill for finding memory used
import os                                       #Import os for memory estimation
import sys                                      #Import sys for terminating the program after the result

minimumf = []                                   # a global list to find the minimum f value after every iteration

class Board:                                    #This class defines the state of the problem in terms of board configuration
	def __init__(self,tiles):
		self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
		self.tiles = tiles
	
	def execute_action(self,action):            #This function returns the resulting state from taking particular action from current state
		new_tiles = self.tiles[:]
		empty_index = new_tiles.index('0')
		if action=='L':	
			if empty_index%self.size>0:
				new_tiles[empty_index-1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-1]
		if action=='R':
			if empty_index%self.size<(self.size-1): 	
				new_tiles[empty_index+1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+1]
		if action=='U':
			if empty_index-self.size>=0:
				new_tiles[empty_index-self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-self.size]
		if action=='D':
			if empty_index+self.size < self.size*self.size:
				new_tiles[empty_index+self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+self.size]
		return Board(new_tiles)
		


class Node:                                             #this class defines each state of the puzzle with level, parent, action and level
    def __init__(self,state,parent,action,position):
        self.state = state
        self.parent = parent
        self.action = action
        self.position = position
    def __repr__(self):
        return str(self.state.tile)
    def __eq__(self, other):
        return self.state.tiles == other.state.tiles

def generate_puzzle(size):                      #Utility function to randomly generate 15-puzzle
	numbers = list(range(size*size))
	random.shuffle(numbers)
	return Node(Board(numbers),None,None)

def get_children(parent_node):                          # This function will generate the children of a node
    children = []
    pos = parent_node.position
    actions = ['L','R','U','D']                         # actions to be performed on parent node to get children
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        child_node = Node(child_state,parent_node,action,pos+1)
        children.append(child_node)
    return children
    
def find_path(node):	                        #This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
	path = []	
	while(node.parent is not None):
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path

def main():                                     #Main function accepting input from console	
    global initial_memory,process,starttime,minimumf,starttime1
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024.0
    initial = str(input("initial configuration: "))                           #fecting the inital state as a string 
    initial_list = initial.split(" ")
    root = Node(Board(initial_list),None,None,0)
    starttime = time.time()                                                   # initializing the start time
    f = root.position+manhattan_distance(root)                                # assigning f value of initial state as a limiter for iterations using manhattan distance
    tmp = 0
    while (True):                                                           # f value will be changed for every loop
        frontier = [root]
        explored = []
        minimumf = []
        while(len(frontier)>0):
            tmp = search(frontier,f,explored)                           #iterative deepening a star search using manhattan distance
        if tmp != 0:
            results(tmp)
            break
        else:
            s = min(minimumf)                                          # find the minimum f value among the nodes 
            f = s
    starttime1 = time.time()
    f1 = root.position+misplaced(root)                                  # assigning f value of initial state as a limiter for iterations using misplaced items
    tmp1 = 0
    while (True):                                                           # f value will be changed for every loop. In this f1 value will be changed
        frontier = [root]
        explored = []
        minimumf = []
        while(len(frontier)>0):
            tmp1 = search1(frontier,f,explored)                           #iterative deepening a star search function using misplaced items
        if tmp1 != 0:
            results1(tmp1)
            break
        else:
            s = min(minimumf)
            f1  = s
    

def results(tmp):                                           #print the results for manhattan
    print("--------------- ID A* search with manhattan distance-----------------")
    (explore,endtime, path) = tmp
    time_taken = endtime-starttime
    print('Moves:',path)
    print('Number of Nodes expanded:',explore)
    print('Time Taken:',time_taken,'seconds')
    final_memory = process.memory_info().rss /1024.0
    print('Memory used:',final_memory-initial_memory,'KB')
    return

def results1(tmp):                                           #print the results for misplaced
    print("--------------- ID A* search with misplaced tiles-----------------")
    (explore,endtime, path) = tmp
    time_taken = endtime-starttime1
    print('Moves:',path)
    print('Number of Nodes expanded:',explore)
    print('Time Taken:',time_taken,'seconds')
    final_memory = process.memory_info().rss /1024.0
    print('Memory used:',final_memory-initial_memory,'KB')

def goal_test(cur_tiles):                                                   #Utility function checking if current state is goal state or not
	return cur_tiles == ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']	

def manhattan_distance(root_node):                                                    #calculates manhattan distance for the current node
    cur_node = []
    for i in [0,4,8,12]:
        cur_node.append(root_node.state.tiles[i:i+4])
    dis = 0
    for row in range(4):
        for col in range(4):
            tile = int(cur_node[row][col])
            x = 0
            y = 0
            if(tile >= 1 and tile <= 4):
                x = tile - 1
                y = 0
            if(tile >= 5 and tile <= 8):
                x = tile - 5
                y = 1
            if(tile >= 9 and tile <= 12):
                x = tile - 9
                y = 2
            if(tile >= 13 and tile <= 15):
                x = tile - 13
                y = 3
            if(tile == 0):
                x = 3
                y = 3
            dis = dis + abs(row - y) + abs(col - x)
    return dis

def search(frontier,f,explored):
    global minimumf
    first_node = frontier.pop() 
    explored.append(first_node)
    if(goal_test(first_node.state.tiles)):                                  #checking whether the node is the expected goal
        endtime = time.time()
        path = find_path(first_node)
        moves = ""
        for letter in path:
            moves = moves + letter
        return (len(explored),endtime,moves)
    if  first_node.position + manhattan_distance(first_node) > f:           # if current nodes f value is greater than the limiter f value then return
        minimumf.append(first_node.position + manhattan_distance(first_node))     #adding the nodes with greater f value to a global variable for finding the minimum f value for iterations
        return 0
    else:
        for child in get_children(first_node):                              #getting the child nodes     
            if child not in explored:
                frontier.append(child)
                tmp = search(frontier,f,explored)                    #recursive function for depth first search
                if isinstance(tmp,int):
                    continue
                else:
                    return tmp
            else:
                continue
    return 0

def search1(frontier,f,explored):
    global minimumf
    first_node = frontier.pop() 
    explored.append(first_node)
    if(goal_test(first_node.state.tiles)):                                  #checking whether the node is the expected goal
        endtime = time.time()
        path = find_path(first_node)
        moves = ""
        for letter in path:
            moves = moves + letter
        return (len(explored),endtime,moves)
    if  first_node.position + misplaced(first_node) > f:                    # if current nodes f value is greater than the limiter f value then return
        minimumf.append(first_node.position + misplaced(first_node))        #adding the nodes with greater f value to a global variable for finding the minimum f value for iterations
        return 0
    else:
        for child in get_children(first_node):                              #getting the child nodes     
            if child not in explored:
                frontier.append(child)
                tmp = search1(frontier,f,explored)                    #recursive function for depth first search
                if isinstance(tmp,int):
                    continue
                else:
                    return tmp
            else:
                continue
    return 0

def misplaced(root_node):                                                   #calculates number of misplaced items in the current node
    goal = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']
    count = 0
    for i in range(0,len(goal)): 
        if(root_node.state.tiles[i] == goal[i]):
            continue
        else:
            count = count + 1
    return count
	
if __name__=="__main__":main()	                                            #main function calling