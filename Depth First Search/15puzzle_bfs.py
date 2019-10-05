import math                         # import math for power operations
import os                           # import os for memory calculations
import time                         # import time for calcultion of time and timeout functionality
import psutil as processdetails     # import psutil for memory calculation. Please check whether the package is available before running
from collections import namedtuple  # import namedtuple from collections


def information(puzzle): #applying the algorithm and printing the output  
    eachState = namedtuple('eachState','current,path')
    frontier = [eachState(puzzle,"")]
    g = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,0]                     # Goal state is written in list 
    past_nodes=[]
    z_index = 0
    ne = 0
    output = []
    route = ""
    timeout = time.time() + 30                                      # Set the timeout for 30 seconds
    while len(frontier)>0 and (time.time() <= timeout):             # loop on the base of length of frontier and timeout
        first = frontier.pop(0)
        node = first.current
        if str(node) == str(g):                                     # Checking whether the current state is the goal state
            output = node[:]
            ne = len(past_nodes)
            route = first.path
            break
        past_nodes.append(node)                                     # appending the current node in to the node history list
        z_index = node.index(0)

        if z_index not in (0,1,2,3):                                #checking whether 0 is in first row for operation UP
            prev = first
            new = []
            new = node[:]
            temp = new[z_index]
            new[z_index] = new[z_index-4]
            new[z_index-4] = temp
            new_state = eachState(new,prev.path + 'U')                # Creating the new namedtuple with new node and direction implemented
            check_frontier = new in [tup.current for tup in frontier] #check whether the new node is in the frontier
            if not check_frontier:
                if new not in past_nodes:                             # Check whether the new node is in node history
                    frontier.append(new_state)                        # if not adding it to the frontier

        if z_index not in (12,13,14,15):                            #checking whether 0 is in last row for operation DOWN
            prev = first
            new = []
            new = node[:]
            temp = new[z_index]
            new[z_index] = new[z_index+4]
            new[z_index+4] = temp
            new_state = eachState(new,prev.path + 'D')
            check_frontier = new in [tup.current for tup in frontier]
            if not check_frontier:
                if new not in past_nodes:
                    frontier.append(new_state)

        if z_index not in (3,7,11,15):                              #checking whether 0 is in last column for operation RIGHT
            prev = first
            new = []
            new = node[:]
            temp = new[z_index]
            new[z_index] = new[z_index+1]
            new[z_index+1] = temp
            new_state = eachState(new,prev.path + 'R')
            check_frontier = new in [tup.current for tup in frontier]
            if not check_frontier:
                if new not in past_nodes:
                    frontier.append(new_state)

        if z_index not in (0,4,8,12):                                   #checking whether 0 is in first coulmn for operation LEFT
            prev = first
            new = []
            new = node[:]
            temp = new[z_index]
            new[z_index] = new[z_index-1] 
            new[z_index-1] = temp
            new_state = eachState(new,prev.path + 'L')
            check_frontier = new in [tup.current for tup in frontier]
            if not check_frontier:
                if new not in past_nodes:
                    frontier.append(new_state)
    if len(output) == 0:                                                # check whether output is empty
        print("Solution not found")
    else:
        print ("Moves:",route)                                          # print the moves
        print ("Number of Nodes expanded:" , ne)                        # print the nodes expanded
          
    

# validating the input based on the availability of 0
def valid(given):
    if 0 not in given:
        return False
    else:
        return True

# START OF THE PROGRAM
intial_state = input('please enter the current state of 15-puzzle with separation by space and assume the empty space as 0: ')
processing_time = time.time()                                           #start the processing time
intial_st_list = intial_state.split()
intial_st_list = [int(x) for x in intial_st_list]                       #Converting the input into a list    
if (valid(intial_st_list)):                                             # Validation check
    information(intial_st_list)
    stop_time=time.time()
    print ("Time Taken:", stop_time - processing_time, "seconds")       # print total time taken
    process = processdetails.Process(os.getpid())                       
    print ("Memory Usage:", str(process.memory_info()[0]/float(math.pow(2,20)))+"KB")  #print total memory used
else:
    print ("Solution not found")