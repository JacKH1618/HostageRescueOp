import heapq, time
import random
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = ( 0,   0,   255)
YELLOW   = ( 255, 255, 153)

width  = 25
height = 25
margin = 1
##size = [708, 708]
size = [(21*26)+1, (29*26)+1]
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
    
class Gridworld(object):
    def __init__(self):
        self.grids = []
        self.swatAgents = []
        self.swatPos = []
        self.swatLastVisited = []
        self.enemyAgents = []
        self.enemyPos = []
        self.enemyLastVisited = []
        self.messages = []
        self.grid_height = 29
        self.grid_width = 21
##        self.filename = ''

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                if x%2==1 and y%2==1:
                    blocked = True
                self.grids.append(Grid_Cell(x, y, blocked))
##        self.enemy = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.enemy = self.get_gridCell(0, 0)
        print('enemy at: %d,%d' % (self.enemy.x, self.enemy.y))
##        self.swat = self.get_grid(random.randint(1,20), random.randint(1,30))
        self.swat = self.get_gridCell(20, 28)

        self.enemyAgents = [Agent(1,1,0*int(width/4)+1,0*int(height/4)+1),
                              Agent(2,1,2*int(width/4)+1,0*int(height/4)+1),
                              Agent(3,1,0*int(width/4)+1,2*int(height/4)+1)]
        self.enemyPos = [self.enemy, self.enemy, self.enemy]
        
        self.swatAgents = [Agent(1,1,int(width/4),int(height/4)),
                              Agent(2,1,3*int(width/4),int(height/4)),
                              Agent(3,1,int(width/4),3*int(height/4))]
        self.swatPos = [self.swat, self.swat, self.swat]

        self.swatLastVisited = [None, None, None]
        self.enemyLastVisited = [None, None, None]

    def get_gridCell(self, x, y):
        return self.grids[x * self.grid_height + y]

    def update_pos(self, agentType, mode, x, y, ind):
        choice = random.randint(1,100)

        if mode == 1:
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
                cell =  self.update_pos(agentType, 1, x, y, ind)
                
            if agentType == 1:
                if(self.swatLastVisited[ind] == cell):
                    cell = self.update_pos(agentType, 1, x, y, ind)
                self.swatLastVisited[ind] = self.get_gridCell(x,y)
            else:
                if(self.enemyLastVisited[ind] == cell):
                    cell = self.update_pos(agentType, 1, x, y, ind)
                self.enemyLastVisited[ind] = self.get_gridCell(x,y)
                
            return cell

    def update_agentPos(self):
        self.swatPos[0] = self.update_pos(1, 1, self.swatPos[0].x, self.swatPos[0].y, 0)
        self.swatPos[1] = self.update_pos(1, 1, self.swatPos[1].x, self.swatPos[1].y, 1)
        self.swatPos[2] = self.update_pos(1, 1, self.swatPos[2].x, self.swatPos[2].y, 2)

        self.enemyPos[0] = self.update_pos(2, 1, self.enemyPos[0].x, self.enemyPos[0].y, 0)
        self.enemyPos[1] = self.update_pos(2, 1, self.enemyPos[1].x, self.enemyPos[1].y, 1)
        self.enemyPos[2] = self.update_pos(2, 1, self.enemyPos[2].x, self.enemyPos[2].y, 2)

    def check_LOS(self):
        for swat in self.swatPos:
            for enemy in self.enemyPos:
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
            
    def display_grid(self):
        pygame.display.set_caption("Rescue Op Simulation")
        screen.fill(BLACK)
        done = False
        for count in range(30):
            
            for grid in self.grids:
                color = BLACK
                if grid.blocked == False:
                    color = WHITE
                #--
                if grid.path == True:
                    color = GREEN
                    grid.path = False
                    
                #--
                if grid == self.enemy:
                    color = YELLOW
                if grid == self.swat:
                    color = YELLOW
                #--
                pygame.draw.rect(screen, color,
                     [(margin+width)*grid.x+margin, (margin+height)*grid.y+margin,
                      width, height])
                
            pygame.draw.rect(screen, RED,
                     [(margin+width)*self.enemyPos[0].x+margin+self.enemyAgents[0].xOffset, (margin+height)*self.enemyPos[0].y+margin+self.enemyAgents[0].yOffset,
                      10, 10])

            pygame.draw.rect(screen, RED,
                     [(margin+width)*self.enemyPos[1].x+margin+self.enemyAgents[1].xOffset, (margin+height)*self.enemyPos[1].y+margin+self.enemyAgents[1].yOffset,
                      10, 10])

            pygame.draw.rect(screen, RED,
                     [(margin+width)*self.enemyPos[2].x+margin+self.enemyAgents[2].xOffset, (margin+height)*self.enemyPos[2].y+margin+self.enemyAgents[2].yOffset,
                      10, 10])

            pygame.draw.circle(screen, BLUE,
                [(self.swatPos[0].x * width)+(self.swatPos[0].x * margin)+self.swatAgents[0].xOffset+1,(self.swatPos[0].y * height)+ (self.swatPos[0].y * margin)+self.swatAgents[0].yOffset+1],4, 0)

            pygame.draw.circle(screen, BLUE,
                [(self.swatPos[1].x * width)+(self.swatPos[1].x * margin)+self.swatAgents[1].xOffset+1,(self.swatPos[1].y * height)+ (self.swatPos[1].y * margin)+self.swatAgents[1].yOffset+1],4, 0)

            pygame.draw.circle(screen, BLUE,
                [(self.swatPos[2].x * width)+(self.swatPos[2].x * margin)+self.swatAgents[2].xOffset+1,(self.swatPos[2].y * height)+ (self.swatPos[2].y * margin)+self.swatAgents[2].yOffset+1],4, 0)
            
            pygame.display.flip()
            time.sleep(1)

            self.update_agentPos()
            self.check_LOS()

def main():
    pygame.init()
##    maze_number = input("Start Y/N: ")
    a = Gridworld()
    a.init_grid()
    a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
