import random                                   #Import random for generating random values
import math                                     #Import math for finding square root
import time                                     #Import time for finding process time span
import psutil                                   #Import psutill for finding memory used
import os                                       #Import os for memory estimation
import sys                                      #Import sys for terminating the program after the result


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
		

		
class Node:                                     #This class defines the node on the search tree, consisting of state, parent and previous action
	def __init__(self,state,parent,action):
		self.state = state
		self.parent = parent
		self.action = action
	
	def __repr__(self):                         #Returns string representation of the state
		return str(self.state.tiles)
	
	def __eq__(self,other):                     #Comparing current node with other node. They are equal if states are equal	
		return self.state.tiles == other.state.tiles
		
def generate_puzzle(size):                      #Utility function to randomly generate 15-puzzle
	numbers = list(range(size*size))
	random.shuffle(numbers)
	return Node(Board(numbers),None,None)

def get_children(parent_node):                  #This function returns the list of children obtained after simulating the actions on current node
	children = []
	actions = ['L','R','U','D']                 # left,right,up,down actions for the given node
	for action in actions:
		child_state = parent_node.state.execute_action(action)
		child_node = Node(child_state,parent_node,action)
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
    global initial_memory,process,starttime
    process = psutil.Process(os.getpid())
    initial_memory = process.memory_info().rss / 1024.0
    initial = str(input("initial configuration: "))                           #fecting the inital state as a string 
    initial_list = initial.split(" ")
    root = Node(Board(initial_list),None,None)
    starttime = time.time()
    d=0
    while (True):                                                             #increasing depth limit for every loop
        if ((time.time()) - starttime > 30):
            print('solution not found')
            break
        iterations=0
        frontier = [root]
        explored = []
        while(len(frontier)>0):
            search(frontier,d,iterations,explored)                           #iterative deepening depth first search function
        d = d+1

def results(explore,endtime,path):                                           #print the results
    time_taken = endtime-starttime
    print('Moves:',path)
    print('Number of Nodes expanded:',explore)
    print('Time Taken:',time_taken,'seconds')
    final_memory = process.memory_info().rss / 1024.0
    print('Memory used:',final_memory-initial_memory,'KB')
    sys.exit()

def goal_test(cur_tiles):                                                   #Utility function checking if current state is goal state or not
	return cur_tiles == ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']	

    

def search(frontier,d,iterations,explored):
    first_node = frontier.pop() 
    explored.append(first_node)
    if(goal_test(first_node.state.tiles)):                                  #checking whether the node is the expected goal
        endtime = time.time()
        path = find_path(first_node)
        moves = ""
        for letter in path:
            moves = moves + letter
        results(len(explored),endtime,moves)
    if d == iterations:
        return
    else:
        iterations = iterations+1
        for child in get_children(first_node):                              #getting the child nodes     
            if child not in explored:
                frontier.append(child)
                search(frontier,d,iterations,explored)                      #recursive function for depth first search
            else:
                continue
    return

	
if __name__=="__main__":main()	                                            #main function calling