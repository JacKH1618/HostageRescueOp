import heapq, time
import random
import pygame
##import easygui

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = ( 0,   0,   255)
YELLOW   = ( 255, 255, 153)
ORANGE   = ( 255, 165, 0)

#Agent Strength Levels
MIN_STRENGTH = 0
MAX_STRENGTH = 100
MAX_STRENGH_DIFF = (MAX_STRENGTH - MIN_STRENGTH)

TRUE = 1
FALSE = 0

CELL_WIDTH  = 25
CELL_HEIGHT = 25
MAX_HEIGHT = 21
MAX_WIDTH = 21
margin = 1
##size = [708, 708]
size = [(MAX_WIDTH*(CELL_WIDTH+1))+1, (MAX_HEIGHT*(CELL_HEIGHT+1))+1]
screen = pygame.display.set_mode(size)

class Grid_Cell(object):
    def __init__(self, x, y, blocked):
        self.blocked = blocked
        self.path = False
        self.x = x
        self.y = y

class Agent(object):
    def __init__(self, agent_id, agent_type, xOffset, yOffset):
        self.agent_id = agent_id
        self.agent_type = agent_type
        self.xOffset = xOffset
        self.yOffset = yOffset
        # Defining strength levels
        if 1 == agent_id:
            self.strength = 10
        elif 2 == agent_id:
            self.strength = 50
        elif 3 == agent_id:
            self.strength = 100
        self.killed = FALSE
    
class Gridworld(object):
    def __init__(self):
        self.grids = []
        self.swatAgents = []
        self.swatPos = []
        self.swatLastVisited = []
        self.enemyAgents = []
        self.enemyPos = []
        self.enemyLastVisited = []
        self.hostagePos = []
        self.messages = []
        self.grid_height = MAX_HEIGHT
        self.grid_width = MAX_WIDTH
        ##Lists of duelling agent objects. duellingSwatList[i] duels with duellingEnemyList[i]
        self.duellingSwatList = []
        self.duellingEnemyList = []
        self.killed = FALSE
##        self.filename = ''

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                if x%2==1 and y%2==1:
                    blocked = True
                self.grids.append(Grid_Cell(x, y, blocked))
##        self.ENEMY_START_POS = self.get_grid(random.randint(1,20), random.randint(1,30))
        # print('self.grids length: %d' % len(self.grids))
        self.ENEMY_START_POS = self.get_gridCell(0, 0)
        #print('enemy at: %d,%d' % (self.ENEMY_START_POS.x, self.ENEMY_START_POS.y))
##        self.SWAT_START_POS = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.SWAT_START_POS = self.get_gridCell(MAX_WIDTH-1, MAX_HEIGHT-1)

        self.enemyAgents = [Agent(1,1,0*int(CELL_WIDTH/4)+1,0*int(CELL_HEIGHT/4)+1),
                              Agent(2,1,2*int(CELL_WIDTH/4)+1,0*int(CELL_HEIGHT/4)+1),
                              Agent(3,1,0*int(CELL_WIDTH/4)+1,2*int(CELL_HEIGHT/4)+1)]
        self.enemyPos = [self.ENEMY_START_POS, self.ENEMY_START_POS, self.ENEMY_START_POS]
        
        self.swatAgents = [Agent(1,2,int(CELL_WIDTH/4),int(CELL_HEIGHT/4)),
                              Agent(2,2,3*int(CELL_WIDTH/4),int(CELL_HEIGHT/4)),
                              Agent(3,2,int(CELL_WIDTH/4),3*int(CELL_HEIGHT/4))]
        self.swatPos = [self.SWAT_START_POS, self.SWAT_START_POS, self.SWAT_START_POS]

        for hst_ind in range(5):
            self.hostagePos.append(self.get_gridCell(random.randrange(1,self.grid_width-1,2), random.randrange(1,(self.grid_height-1)/2,2)))

        self.swatLastVisited = [None, None, None]
        self.enemyLastVisited = [None, None, None]

    def get_gridCell(self, x, y):
        return self.grids[x * self.grid_height + y]

    def take_action(self, agentType, mode, x, y, ind):

        if agentType == 1:
            rescued = False
            for hst_ind in range(len(self.hostagePos)):
                if (x-1 >= 0 and self.hostagePos[hst_ind] == self.get_gridCell(x-1,y) or
                    y-1 >= 0 and self.hostagePos[hst_ind] == self.get_gridCell(x,y-1) or
                    x+1 <= self.grid_width-1 and self.hostagePos[hst_ind] == self.get_gridCell(x+1,y) or
                    y+1 <= self.grid_height-1 and self.hostagePos[hst_ind] == self.get_gridCell(x,y+1)):
##                    self.hostagePos[hst_ind] = self.SWAT_START_POS
                    self.hostagePos.remove(self.hostagePos[hst_ind])
                    rescued = True
                    if rescued :
                        return self.get_gridCell(x,y)

        if mode == 1:
            choice = random.randint(1,100)
            if choice <= 25:
                if (x-1 < 0):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x-1,y)
            elif choice <= 50:
                if (y-1 < 0):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x,y-1)
            elif choice <= 75:
                if (x+1 > self.grid_width-1):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x+1,y)
            else:
                if (y+1 > self.grid_height-1):
                    cell = self.get_gridCell(x,y)
                else:
                    cell = self.get_gridCell(x,y+1)

            if cell.blocked == True or cell == self.get_gridCell(x,y):
                cell =  self.take_action(agentType, 1, x, y, ind)
                
            if agentType == 1:
                if(self.swatLastVisited[ind] == cell):
                    cell = self.take_action(agentType, 1, x, y, ind)
                self.swatLastVisited[ind] = self.get_gridCell(x,y)
            else:
                if(self.enemyLastVisited[ind] == cell):
                    cell = self.take_action(agentType, 1, x, y, ind)
                self.enemyLastVisited[ind] = self.get_gridCell(x,y)
                
            return cell

    def update_agentPos(self):
        for swat_ind in range(len(self.swatPos)):
            self.swatPos[swat_ind] = self.take_action(1, 1, self.swatPos[swat_ind].x, self.swatPos[swat_ind].y, swat_ind)

        for enemy_ind in range(len(self.enemyPos)):
            self.enemyPos[enemy_ind] = self.take_action(2, 1, self.enemyPos[enemy_ind].x, self.enemyPos[enemy_ind].y, enemy_ind)

    def check_LOS(self):
        for swatindex, swat in enumerate(self.swatPos):
            for enemyindex, enemy in enumerate(self.enemyPos):
                if (FALSE == self.swatAgents[swatindex].killed) and (FALSE == self.enemyAgents[enemyindex].killed):
                    if(swat.x == enemy.x and swat.x%2 == 0):
                        self.get_gridCell(swat.x, swat.y).path = True
                        self.get_gridCell(enemy.x, enemy.y).path = True
                        diff = enemy.y - swat.y
                        while diff!=0:
                            self.get_gridCell(swat.x, swat.y+diff).path = True
                            if diff > 0:
                                diff = diff-1
                            else:
                                diff = diff+1
                        ##Adding the opposing agents in LOS to duelling lists
                        self.duellingSwatList.append(self.swatAgents[swatindex])
                        self.duellingEnemyList.append(self.enemyAgents[enemyindex])
                        

                    if(swat.y == enemy.y and swat.y%2 == 0):
                        self.get_gridCell(swat.x, swat.y).path = True
                        self.get_gridCell(enemy.x, enemy.y).path = True
                        diff = enemy.x - swat.x
                        while diff!=0:
                            self.get_gridCell(swat.x+diff, swat.y).path = True
                            if diff > 0:
                                diff = diff-1
                            else:
                                diff = diff+1

    def duel(self):
        ##temp = 1
        ##easygui.msgbox("Time for some shootin'!", title="Duel!")
        for duelindex in range(len(self.duellingSwatList)):
            ## Lengths of duellingSwatList and duellingEnemyList should be equal

            ## Calculate probability of swat killing enemy (or vice versa)
            #prob_swatKillsEnemy = self.duellingSwatList[duelindex].strength/MAX_STRENGTH
            #prob_enemyKillsSwat = self.duellingEnemyList[duelindex].strength/MAX_STRENGTH

            ## Kill none, one or both depending on probablity based on agent's strength level
            rand_num = random.randint(1,100)
            if rand_num <= self.duellingSwatList[duelindex].strength:
                ## Add code for deleting enemy agent object pointed to by duellingEnemyList[duelindex]
                self.duellingEnemyList[duelindex].killed = TRUE
                
            if rand_num <= self.duellingEnemyList[duelindex].strength:
                ## Add code for deleting swat agent object pointed to by duellingSwatList[duelindex]
                self.duellingSwatList[duelindex].killed = TRUE

        ## Cleanup deulling lists for next use
        for duelindex in range(len(self.duellingSwatList)):
            del(self.duellingSwatList[duelindex])
            del(self.duellingEnemyList[duelindex])
            
        
            
    def display_grid(self):
        pygame.display.set_caption("Rescue Op Simulation")
        screen.fill(BLACK)
        done = False
        for count in range(100):
####            Display GridWorld
            for grid in self.grids:
                color = BLACK
                if grid.blocked == False:
                    color = WHITE
                #--
                if grid.path == True:
                    color = GREEN
                    grid.path = False
                    
                #--
                if grid == self.ENEMY_START_POS:
                    color = YELLOW
                if grid == self.SWAT_START_POS:
                    color = YELLOW
                #--
                pygame.draw.rect(screen, color,
                     [(margin+CELL_WIDTH)*grid.x+margin, (margin+CELL_HEIGHT)*grid.y+margin,
                      CELL_WIDTH, CELL_HEIGHT])
            
##-- Display Enemy Agents
            for enemy_ind in range(len(self.enemyPos)):
                if FALSE == self.enemyAgents[enemy_ind].killed:
                    pygame.draw.rect(screen, RED,
                         [(margin+CELL_WIDTH)*self.enemyPos[enemy_ind].x+margin+self.enemyAgents[enemy_ind].xOffset, (margin+CELL_HEIGHT)*self.enemyPos[enemy_ind].y+margin+self.enemyAgents[enemy_ind].yOffset,
                          10, 10])

##-- Display Swat Agents
            for swat_ind in range(len(self.swatPos)):
                if FALSE == self.swatAgents[swat_ind].killed:
                    pygame.draw.circle(screen, BLUE,
                    [(self.swatPos[swat_ind].x * CELL_WIDTH)+(self.swatPos[swat_ind].x * margin)+self.swatAgents[swat_ind].xOffset+1,(self.swatPos[swat_ind].y * CELL_HEIGHT)+ (self.swatPos[swat_ind].y * margin)+self.swatAgents[swat_ind].yOffset+1],4, 0)

##-- Display Hostages
            for hst_ind in range(len(self.hostagePos)):
                pygame.draw.circle(screen, ORANGE,
                    [(self.hostagePos[hst_ind].x * CELL_WIDTH)+(self.hostagePos[hst_ind].x * margin)+int(CELL_WIDTH/2)+1,(self.hostagePos[hst_ind].y * CELL_HEIGHT)+ (self.hostagePos[hst_ind].y * margin)+int(CELL_HEIGHT/2)+1],4,0)
            
            pygame.display.flip()
            time.sleep(0.5)

            self.update_agentPos()
            self.check_LOS()
            self.duel()

def main():
    pygame.init()
##    maze_number = input("Start Y/N: ")
    a = Gridworld()
    a.init_grid()
    a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
