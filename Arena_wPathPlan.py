import heapq, time
import random
import pygame

BLACK    = (   0,   0,   0)
WHITE    = ( 255, 255, 255)
RED      = ( 255,   0,   0)
GREEN    = (   0, 255,   0)
BLUE     = ( 0,   0,   255)
YELLOW   = ( 255, 255, 153)

GRID_HEIGHT = 21
GRID_WIDTH = 29

width  = 25
height = 25
margin = 1
##size = [708, 708]
size = [(GRID_HEIGHT*26)+1, (GRID_WIDTH*26)+1]
screen = pygame.display.set_mode(size)

class GridCell(object):
    def __init__(self, x, y, blocked):
        self.blocked = blocked
        self.path = False
        self.x = x
        self.y = y

class Agent(object):
    def __init__(self, agenr_id, agent_type):
        self.agent_id = agent_id
        self.agent_type = agent_type
    
class Gridworld(object):
    def __init__(self):
        self.grids = []
        self.agents = []
        self.agentPos = []
        self.grid_height = GRID_HEIGHT
        self.grid_width = GRID_WIDTH
##        self.filename = ''

    def init_grid(self):
        for x in range(self.grid_width):
            for y in range(self.grid_height):
                blocked = False
                if x%2==1 and y%2==1:
                    blocked = True
                self.grids.append(GridCell(x, y, blocked))
##        self.enemy = self.get_gridcell(random.randint(1,20), random.randint(1,30))
        self.enemy = self.get_gridcell(0, 0)
        print('enemy at: %d,%d' % (self.enemy.x, self.enemy.y))
##        self.swat = self.get_gridcell(random.randint(1,20), random.randint(1,30))
        self.swat = self.get_gridcell(GRID_HEIGHT-1, GRID_WIDTH-1)

    def get_gridcell(self, x, y):
        return self.grids[x * self.grid_height + y]

##    def check_LOS():
            
    def display_grid(self):
        pygame.display.set_caption("Rescue Op Simulation")
        screen.fill(BLACK)
        done = False
        for count in range(5):
            self.enemyAt = self.get_gridcell(random.randrange(0,self.grid_width-1,2), random.randrange(0,self.grid_height-1,2))        

            self.swatAt = self.get_gridcell(random.randrange(0,self.grid_width-1,2), random.randrange(0,self.grid_height-1,2))        

            if (self.enemyAt.x == self.swatAt.x):
                self.enemyAt.path = True
                self.swatAt.path = True
                diff = self.enemyAt.y - self.swatAt.y
                while diff!=0:
                    self.markGrid = self.get_gridcell(self.swatAt.x , self.swatAt.y+diff)
                    self.markGrid.path = True
                    if diff > 0:
                        diff = diff-1
                    else:
                        diff = diff+1

            if (self.enemyAt.y == self.swatAt.y):
                self.enemyAt.path = True
                self.swatAt.path = True
                diff = self.enemyAt.x - self.swatAt.x
                while diff!=0:
                    self.markGrid = self.get_gridcell(self.swatAt.x+diff , self.swatAt.y)
                    self.markGrid.path = True
                    if diff > 0:
                        diff = diff-1
                    else:
                        diff = diff+1
            
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
    ##            pygame.draw.circle(screen, RED,
    ##                [(margin+width)*(self.enemy.x+margin), (margin+height)*(self.enemy.y+margin)],5, 0)
    ##            pygame.display.flip()
            pygame.draw.circle(screen, RED,
                [(self.enemyAt.x * width)+(self.enemyAt.x * margin)+int(width/4)+1,(self.enemyAt.y * height)+ (self.enemyAt.y * margin)+int(height/4)+1],4, 0)

            pygame.draw.circle(screen, RED,
                [(self.swatAt.x * width)+(self.swatAt.x * margin)+int(3*width/4)+1,(self.swatAt.y * height)+ (self.swatAt.y * margin)+int(height/4)+1],4, 0)
            
            pygame.display.flip()
            time.sleep(2)

def main():
    pygame.init()
    a = Gridworld()
    a.init_grid()
    a.display_grid()
    pygame.quit()
    
if __name__ == '__main__':
    main()
