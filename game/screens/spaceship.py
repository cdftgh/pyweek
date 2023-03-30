
import pygame
import random
from mpmath import *
pi = 3.1415926535897932384626433832795028841971693#99375105820974944592307816406286208998628034825342117067

class GameScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 50)

        self.arr = []
        self.backgrounds=[]

        self.background = pygame.image.load(r"pyweek\BersFork2\game\images\first_room.png")
        self.backgrounds.append(self.background)
        self.background = pygame.transform.scale(self.background, (width, height))

        key = pygame.image.load(r"pyweek\BersFork2\game\images\key.png")
        self.key = pygame.transform.scale(key, (25, 30))
        self.battery=10000000
        self.used=0
        self.xkey=random.randint(0,self.width-30)
        self.ykey=random.randint(0,self.height-30)
        self.gotkey=0
        self.widthkey=25
        self.heightkey=30

        powerbox = pygame.image.load(r"pyweek\BersFork2\game\images\power_box.png")
        self.powerbox = pygame.transform.scale(powerbox, (160, 200)) # This goes at (320, 180)

        self.deathText = pygame.image.load(r"pyweek\BersFork2\game\images\death_text.png")
        self.deathText = pygame.transform.scale(self.deathText, (604, 480))
        self.prevangleis=0
        self.tentatives=40
        self.start=0
        self.waittimes=0

        battery = pygame.image.load(r"pyweek\BersFork2\game\images\battery.png")
        self.battery = pygame.transform.scale(battery, (35, 50))

    def display(self,lighton,radius,clicked):
        self.screen.fill([0, 0, 0])

        a, b = pygame.mouse.get_pos()
        # put objects onto the background before calling array3d()
        if not self.gotkey :
            self.background.blit(self.key, (self.xkey, self.ykey))
            if clicked:
                self.clickedkey(a,b)
        else:
            if self.tentatives > 0:
                self.turning((300, 200), 30, 60, (a, b))
        color = (255*self.used/self.battery, 255*(1-self.used/self.battery), 0)
        # battery place here

        # Drawing Rectangle
        pygame.draw.rect(self.screen, color, pygame.Rect(self.width*1/3, 0, self.width/3*(1-self.used/self.battery), 60))

        # use native pygame functions to convert to a pixel array
        self.arr = pygame.surfarray.array3d(self.background)

        #if a < self.arr.shape[0] - self.radius and b < self.arr.shape[1] + self.radius:
        if lighton and random.random()<0.95 and self.used/self.battery<1:
            self.used+=1*radius*radius*pi
            self.see(self.screen, a, b,radius, self.arr)
            
        elif self.used/self.battery>=1:
            self.screen.blit(self.deathText, (0, 0))

    def see(self, screen, a, b, radius, pixels):
        for i in range(max(0,a - radius),min(self.arr.shape[0], a + radius)):
            # fixes error if moving the cursor down off the screen
            for j in range(max(0, b - radius), min(self.arr.shape[1], b + radius)):
                if ((i - a) ** 2 + (j - b) ** 2) ** 0.5 < radius:
                    pygame.draw.line(screen, pixels[i][j], (i, j), (i, j))

    def clickedkey(self,a,b):
        if a>self.xkey and a<self.widthkey+self.xkey and b>self.ykey and b<self.heightkey+self.ykey:
            self.gotkey=1
            self.background = pygame.image.load(r"pyweek\BersFork2\game\images\first_room.png")
            self.background = pygame.transform.scale(self.background, (self.width, self.height))
            self.used /= 2
    def turning(self,rotation_point,radiusmin,radiusmax,mousepoint):

        radius=((mousepoint[1]-rotation_point[1])**2+(mousepoint[0]-rotation_point[0])**2)**0.5
        nowangle=degrees(atan((mousepoint[1]-rotation_point[1])/(0.001+(mousepoint[0]-rotation_point[0]))))
        if nowangle==self.prevangleis:
            self.waittime+=1
        else:
            self.waittime=0
        if radiusmax>=radius and radius>=radiusmin and ((nowangle<=self.prevangleis and nowangle<=0) or (self.prevangleis>=nowangle and nowangle>=0) or abs(nowangle)==90 ) and self.waittime<10:
            pygame.draw.circle(self.screen, (0,255,0), rotation_point, radiusmax,radiusmax-radiusmin)
            self.start+=1# (r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.
        else:
            if self.start>2:
                self.start/=1.2

            pygame.draw.circle(self.screen, (255,0,0), rotation_point, radiusmax,radiusmax-radiusmin) # (r, g, b) is color, (x, y) is center, R is radius and w is the thickness of the circle border.

        self.prevangleis=nowangle
        print(self.start)

        pass