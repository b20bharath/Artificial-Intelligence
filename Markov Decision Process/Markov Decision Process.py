import random                                   #Import random for generating random values
import sys
ter_states = []                                 #list of terminal states

def main():                                     #main function
    global ter_states
    name = input('Enter file name:')
    fh = open(name)                             #file handle for reading the input values from the file
    size = []
    walls = []
    reward = 0
    prob = []
    dis_rate = 0
    epsilon = 0
    for line in fh:                                                         #looping each line
        line = line.rstrip()
        if line.startswith('size :'):                                       #size of the environment
            words = line.split()
            size.append(int(words[3]))
            size.append(int(words[2]))
        if line.startswith('walls :'):                                      #location of walls
            words1 = line.split(':')
            words2 = words1[1].split(',')
            for word in words2:
                word = word.strip()
                words = word.split()
                walls.append([int(words[1])-1,int(words[0])-1])
        if line.startswith('terminal_states : '):                           #location of terminal states and corresponding rewards
            words1 = line.split(':')
            words2 = words1[1].split(',')
            for word in words2:
                word = word.strip()
                words = word.split()
                ter_states.append([int(words[1]) - 1,int(words[0]) - 1,int(words[2])])
        if line.startswith('reward :'):                                     #reward for normal states
            words = line.split()
            reward = float(words[2])
        if line.startswith('transition_probabilities :'):                   #probability distribution of each action
            words = line.split()
            prob.append(float(words[2]))
            prob.append(float(words[3]))
            prob.append(float(words[4]))
            prob.append(float(words[5]))
        if line.startswith('discount_rate :'):                              # gamma value
            words = line.split()
            dis_rate = float(words[2])
        if line.startswith('epsilon :'):                                    #epsilon value
            words = line.split()
            epsilon = float(words[2])
    grid = []
    for i in range(size[0]):
        col = []
        for j in range(size[1]):
            col.append(0)
        grid.append(col)
    
    fh1 = open('output.txt','w+')                                           #file handle for writing the output
    
    for wall in walls:
        grid[wall[0]][wall[1]] = 'null'
    oldgrid = []
    
    for ter in ter_states:
        grid[ter[0]][ter[1]] = ter[2]
    
    for i in range(len(grid)):
        col = []
        for j in range(len(grid[0])):
            if(isTerminal(i,j)):
                col.append(0)
            else:
                col.append(grid[i][j])
        oldgrid.append(col)
    policygrid = []

    for i in range(len(grid)):
        col = []
        col = grid[i].copy()
        policygrid.append(col)
    

    # value iteration for each state in given environment
    cycle = 0
    while(True):
        delta = 0.0
        for i in range(len(oldgrid)):
            for j in range(len(oldgrid[0])):
                if(oldgrid[i][j] == 'null'):
                    grid[i][j] = oldgrid[i][j]
                    continue
                if(isTerminal(i,j)):
                    continue
                #computing utility values of each action
                action_up = (prob[0]*utility(oldgrid,i,j,i+1,j))+(prob[1]*utility(oldgrid,i,j,i,j+1))+(prob[2]*utility(oldgrid,i,j,i,j-1))+(prob[3]*utility(oldgrid,i,j,i-1,j))
                action_down = (prob[0]*utility(oldgrid,i,j,i-1,j))+(prob[1]*utility(oldgrid,i,j,i,j+1))+(prob[2]*utility(oldgrid,i,j,i,j-1))+(prob[3]*utility(oldgrid,i,j,i+1,j))
                action_right = (prob[0]*utility(oldgrid,i,j,i,j+1))+(prob[1]*utility(oldgrid,i,j,i+1,j))+(prob[2]*utility(oldgrid,i,j,i-1,j))+(prob[3]*utility(oldgrid,i,j,i,j-1))
                action_left = (prob[0]*utility(oldgrid,i,j,i,j-1))+(prob[1]*utility(oldgrid,i,j,i+1,j))+(prob[2]*utility(oldgrid,i,j,i-1,j))+(prob[3]*utility(oldgrid,i,j,i,j+1))
                #find the max
                maximum = max(action_up,action_down,action_right,action_left)
                grid[i][j] = (maximum*dis_rate) + reward
        for i in range(len(oldgrid)):
            for j in range(len(oldgrid[0])):
                if(grid[i][j] != 'null' and abs(grid[i][j] - oldgrid[i][j]) > delta):
                    delta = abs(grid[i][j] - oldgrid[i][j])
        
        # conversion the grid 
        printgrid = []
        k = len(oldgrid)
        count1 = 0
        while (k>0):
            printgrid.append([])
            for item in oldgrid[k-1]:
                printgrid[count1].append(item)
            count1 = count1 + 1
            k = k - 1
        # writing the grid in to file

        fh1.write('Iteration : %d\n' % cycle)
        for lst in printgrid:
            for item in lst:
                fh1.write('%s ' % str(item))
            fh1.write('\n')
        fh1.write('\n')

        cycle = cycle+1
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                oldgrid[i][j] = grid[i][j]
        
        if(delta > (epsilon * ((1 - dis_rate)/dis_rate))):
            continue
        else:
            break                                                    #if the maximum differnce is < delta then stop the cycle
    
    # conversion the grid 
    finalgrid = []
    k = len(oldgrid)
    count1 = 0
    while (k>0):
        finalgrid.append([])
        for item in oldgrid[k-1]:
            finalgrid[count1].append(item)
        count1 = count1 + 1
        k = k - 1
    # writing the grid in to file
    fh1.write('Final Value After Convergence\n')
    for lst in finalgrid:
        for item in lst:
            fh1.write('%s ' % str(item))
        fh1.write('\n')
    fh1.write('\n')
    #final policy of value iteration
    final = finalpolicy(oldgrid)
    fh1.write('Final policy of value iteration:\n')
    # conversion the final policy of value iteration
    vgrid = []
    f = len(final)
    count2 = 0
    while (f>0):
        vgrid.append([])
        for item in final[f-1]:
            vgrid[count2].append(item)
        count2 = count2 + 1
        f = f - 1
    # writing the grid in to file
    for lst in vgrid:
        for item in lst:
            fh1.write('%s ' % str(item))
        fh1.write('\n')
    fh1.write('\n')

    # modified policy iteration
    actions = ['N', 'S', 'E', 'W']
    actiongrid = []
    for i in range(size[0]):                                            #randomly choosing an action for each state
        col = []
        for j in range(size[1]):
            col.append(random.choice(actions))
        actiongrid.append(col)
    
    for wall in walls:
        actiongrid[wall[0]][wall[1]] = '-'
    for ter in ter_states:
        actiongrid[ter[0]][ter[1]] = 'T'

    while(True):
        unchanged = True
        policygrid = policyevaluation(actiongrid,policygrid,prob,dis_rate,reward)
        for i in range(len(policygrid)):
            for j in range(len(policygrid[0])):
                if(policygrid[i][j] == 'null'):
                    grid[i][j] = oldgrid[i][j]
                    continue
                if(isTerminal(i,j)):
                    continue
                #action with maximum utility is selected
                act1 = 0
                act_up = (prob[0]*utility(policygrid,i,j,i+1,j))+(prob[1]*utility(policygrid,i,j,i,j+1))+(prob[2]*utility(policygrid,i,j,i,j-1))+(prob[3]*utility(policygrid,i,j,i-1,j))
                act_down = (prob[0]*utility(policygrid,i,j,i-1,j))+(prob[1]*utility(policygrid,i,j,i,j+1))+(prob[2]*utility(policygrid,i,j,i,j-1))+(prob[3]*utility(policygrid,i,j,i+1,j))
                act_right = (prob[0]*utility(policygrid,i,j,i,j+1))+(prob[1]*utility(policygrid,i,j,i+1,j))+(prob[2]*utility(policygrid,i,j,i-1,j))+(prob[3]*utility(policygrid,i,j,i,j-1))
                act_left = (prob[0]*utility(policygrid,i,j,i,j-1))+(prob[1]*utility(policygrid,i,j,i+1,j))+(prob[2]*utility(policygrid,i,j,i-1,j))+(prob[3]*utility(policygrid,i,j,i,j+1))

                if(act_up>act_down and act_up>act_right and act_up>act_left):
                    act1 = 'N'
                if(act_down>act_up and act_down>act_left and act_down>act_right):
                    act1 = 'S'
                if(act_right>act_down and act_right>act_left and act_right>act_up):
                    act1 = 'E'
                if(act_left>act_up and act_left>act_down and act_left>act_right):
                    act1 = 'W'
                
                if (act1 != actiongrid[i][j]):                          #random action is compared with the chosen action
                    actiongrid[i][j] = act1
                    unchanged = False
        if(unchanged):
            break
    
    fh1.write('\n------------------------------------------\n')
    fh1.write('Optimal policy after modified policy iteration:\n')
    # conversion the optimal policy 
    pgrid = []
    f = len(actiongrid)
    count1 = 0
    while (f>0):
        pgrid.append([])
        for item in actiongrid[f-1]:
            pgrid[count1].append(item)
        count1 = count1 + 1
        f = f - 1
    # writing the grid in to file
    for lst in pgrid:
        for item in lst:
            fh1.write('%s ' % str(item))
        fh1.write('\n')
    fh1.write('\n')



    print('------Output.txt is generated------')

    
def policyevaluation(actiongrid,policygrid,prob,dis_rate,reward,k=21):                  #policy evaluation for the states with randomly choosen actions
    for p in range(k):
        for i in range(len(policygrid)):
            for j in range(len(policygrid[0])):
                if(policygrid[i][j] == 'null'):
                    continue
                if(isTerminal(i,j)):
                    continue
                act = actiongrid[i][j]
                value = 0
                #value is set for each action
                if(act == 'N'):
                    value = (prob[0]*utility(policygrid,i,j,i+1,j))+(prob[1]*utility(policygrid,i,j,i,j+1))+(prob[2]*utility(policygrid,i,j,i,j-1))+(prob[3]*utility(policygrid,i,j,i-1,j))
                if(act == 'S'):
                    value = (prob[0]*utility(policygrid,i,j,i-1,j))+(prob[1]*utility(policygrid,i,j,i,j+1))+(prob[2]*utility(policygrid,i,j,i,j-1))+(prob[3]*utility(policygrid,i,j,i+1,j))
                if(act == 'E'):
                    value = (prob[0]*utility(policygrid,i,j,i,j+1))+(prob[1]*utility(policygrid,i,j,i+1,j))+(prob[2]*utility(policygrid,i,j,i-1,j))+(prob[3]*utility(policygrid,i,j,i,j-1))
                if(act == 'W'):
                    value = (prob[0]*utility(policygrid,i,j,i,j-1))+(prob[1]*utility(policygrid,i,j,i+1,j))+(prob[2]*utility(policygrid,i,j,i-1,j))+(prob[3]*utility(policygrid,i,j,i,j+1))
                policygrid[i][j] = (value*dis_rate)+reward                              #the expected utility value is caluclated for the given action              
    return policygrid                                                                   #return the updated policy
                
        


def finalpolicy(grid):
    final = []
    for i in range(len(grid)):
        col = []
        for j in range(len(grid[0])):
            d = getdirection(grid,i,j)
            col.append(d)
        final.append(col)
    return final

def getdirection(grid,x,y):
    row = len(grid)
    col = len(grid[0])
    if grid[x][y] == 'null':
        return '-'
    if (isTerminal(x,y)):
        return 'T'
    north = -(sys.maxsize)
    west = -(sys.maxsize)
    east = -(sys.maxsize)
    south = -(sys.maxsize)
    highest = []
    if((x+1)<row and grid[x+1][y] != 'null'):
        north = grid[x+1][y]
    if((x-1) >=0 and grid[x-1][y] != 'null'):
        south = grid[x-1][y]
    if((y-1)>=0 and grid[x][y-1] != 'null'):
        west = grid[x][y-1]
    if((y+1) < col and grid[x][y+1] != 'null'):
        east = grid[x][y+1]
    act1 = 0
    if(north>south and north>east and north>west):
        act1 = 'N'
    if(south>north and south>west and south>east):
        act1 = 'S'
    if(east>south and east>west and east>north):
        act1 = 'E'
    if(west>north and west>south and west>east):
        act1 = 'W'
    return act1




def utility(grid,x,y,a_x,a_y):                                  #return the utility value for an action
    row = len(grid)
    col = len(grid[0])
    if(a_x < 0):
        a_x = 0
    if(a_x == row):
        a_x = row -1 
    if(a_y < 0):
        a_y = 0
    if(a_y == col):
        a_y = col - 1
    if(grid[a_x][a_y] == 'null'):                               #if the transition state is a wall it will return the same value
        return grid[x][y]
    return grid[a_x][a_y]

   
    


def isTerminal(x,y):                                            # checks whether the current state is a terminal state
    for lst in ter_states:
        if (x == lst[0] and y == lst[1]):
            return True
    return False




if __name__=="__main__":main()                                  # calling main function