import random                                   #Import random for generating random values
import math                                     #Import math for finding square root
import time                                     #Import time for finding process time span
import psutil                                   #Import psutill for finding memory used
import os                                       #Import os for memory estimation
import sys                                      #Import sys for terminating the program after the result
import multiprocessing                          #import multiprocessing to start different processes


class Board:                                    #This class defines the state of the problem in terms of board configuration
	def __init__(self,tiles):
		self.size = int(math.sqrt(len(tiles)))  # defining length/width of the board
		self.tiles = tiles
	
	def execute_action(self,action):            #This function returns the resulting state from taking particular action from current state
		new_tiles = self.tiles[:]
		empty_index = new_tiles.index('0')
		if action=='L':	                        #performing action left
			if empty_index%self.size>0:
				new_tiles[empty_index-1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-1]
		if action=='R':                         #performing action right
			if empty_index%self.size<(self.size-1): 	
				new_tiles[empty_index+1],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+1]
		if action=='U':                         #performing action up
			if empty_index-self.size>=0:
				new_tiles[empty_index-self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index-self.size]
		if action=='D':                         #performing action down
			if empty_index+self.size < self.size*self.size:
				new_tiles[empty_index+self.size],new_tiles[empty_index] = new_tiles[empty_index],new_tiles[empty_index+self.size]
		return Board(new_tiles)
		
class Node:                                     #this class defines each state of the puzzle with level, parent and action 
    def __init__(self,state,parent,action,position):
        self.state = state
        self.parent = parent
        self.position = position
        self.action = action

    def __repr__(self):
        return str(self.state.tiles)

    def __eq__(self,other):
        return self.state.tiles == other.state.tiles
		
		
def generate_puzzle(size):                      #Utility function to randomly generate 15-puzzle
	numbers = list(range(size*size))
	random.shuffle(numbers)
	return Node(Board(numbers),None,None)

def get_children(parent_node):                  #fetches all children nodes from the parend node
    children = []
    pos = int(parent_node.position)
    actions = ['L','R','U','D']
    for action in actions:
        child_state = parent_node.state.execute_action(action)
        child_node = Node(child_state,parent_node,action,pos + 1)
        children.append(child_node)
    return children
        

def find_path(node):	                        #This function backtracks from current node to reach initial configuration. The list of actions would constitute a solution path
	path = []	
	while(node.parent is not None):
		path.append(node.action)
		node = node.parent
	path.reverse()
	return path

def main():
    initial = str(input("initial configuration: "))                           #fecting the inital state as a string 
    initial_list = initial.split(" ")
    root = Node(Board(initial_list),None,None,0)
    p1 = multiprocessing.Process(target=astar_misplaced,args=[root])            #assigning first process for misplaced
    p2 = multiprocessing.Process(target=astar_manhattan,args=[root])            #assigning second process for manhattan
    print("----------------A* star search using Number of misplaced tiles---------------")
    befor1 = time.time()
    p1.start()                                                                  #starting of first process
    p1.join()                                                                   #stoping of first process
    after1 = time.time()
    print("Time Taken",after1-befor1,"Seconds")
    print("----------------A* star search using Manhattan Distance--------------------")
    befor2 = time.time()
    p2.start()                                                                  #starting of second process
    p2.join()                                                                   #stoping of second process
    after2 = time.time()
    print("Time Taken",after2-befor2, "Seconds")
    

def misplaced(root_node):                                                   #calculates number of misplaced items in the current node
    goal = ['1','2','3','4','5','6','7','8','9','10','11','12','13','14','15','0']
    count = 0
    for i in range(0,len(goal)):
        if(root_node.state.tiles[i] == goal[i]):
            continue
        else:
            count = count + 1
    return count

def distance(root_node):                                                    #calculates manhattan distance for the current node
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

def memory():                                                       #gives us the current memory information
    process = psutil.Process(os.getpid())
    memory_cur = process.memory_info().rss / 1024.0
    return memory_cur

def astar_manhattan(root):                                          # perform a star search using manahattan distance
    m1 = memory()
    starttime = time.time()
    frontier = []
    frontier.append(root)
    expanded = 0
    explored = []
    explored.append(root)
    min_node = Node(None,None,None,None)

    while (len(frontier)>0):                                    
        curtime = time.time()
        if (curtime-starttime > 30):                                        # setting a timeout of 30 seconds
            print("Solution not found")
            return
        minimum = sys.maxsize
        for i in range(0,len(frontier)):
            start_node = frontier[i]
            m = distance(start_node)
            if(m + start_node.position < minimum):                          #calculating the minimum f value
                min_node = start_node 
                minimum = m + start_node.position
        z = frontier.index(min_node)
        frontier.pop(z)
        if (distance(min_node) == 0):
            path = find_path(min_node)
            moves = ""
            for i in path:
                moves = moves + i
            print("Moves:", moves)
            print("Number of Nodes expanded:", len(explored))
            m2 = memory()
            print("Memory usage",m2-m1,"KB")
            return
        else:
            expanded = expanded + 1
            children = get_children(min_node)
            for child in children:
                if child not in explored:
                    explored.append(child)
                    frontier.append(child)                                  # appending the child node to the frontier
                else:
                    continue
    return 0


def astar_misplaced(root):                                                  # perform a star search using number of tiles misplaced
    m1 = memory()
    starttime = time.time()
    frontier = []
    frontier.append(root)
    expanded = 0
    explored = []
    explored.append(root)
    min_node = Node(None,None,None,None)
    while (len(frontier)>0):
        curtime = time.time()
        if (curtime-starttime > 30):                                        # setting a timeout of 30 seconds
            print("Solution not found")
            return
        minimum = sys.maxsize
        for i in range(0,len(frontier)):
            start_node = frontier[i]
            m = misplaced(start_node)
            if(m + start_node.position < minimum):
                min_node = start_node
                minimum = m + start_node.position
        z = frontier.index(min_node)
        frontier.pop(z)
        if (misplaced(min_node) == 0):                                      #calculating the minimum f value
            path = find_path(min_node)
            moves = ""
            for i in path:
                moves = moves + i
            print("Moves:", moves)
            print("Number of Nodes expanded:", len(explored))
            m2 = memory()
            print("Memory Usage",m2 - m1,"KB")
            return
        else:
            expanded = expanded + 1
            children = get_children(min_node)
            for child in children:
                if child not in explored:
                    explored.append(child)
                    frontier.append(child)                                  # appending the child node to the frontier
                else:
                    continue
    return 0


if __name__=="__main__":main()	                                            #main function calling