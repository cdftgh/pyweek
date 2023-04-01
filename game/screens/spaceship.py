
import pygame
import random
from mpmath import *

pi = 3.1415926535897932384626433832795028841971693993751#05820974944592307816406286208998628034825342117067

class GameScreen:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 50)
        self.seconds = 0
        self.previous_second = 0

        self.arr = []
        self.backgrounds=[]

        self.background = pygame.image.load(r"game\images\first_room.png")
        self.backgrounds.append(self.background)
        self.background = pygame.transform.scale(self.background, (width, height))

        key = pygame.image.load(r"game\images\key.png")
        self.key = pygame.transform.scale(key, (25, 30))
        self.battery=10000000
        self.used=0
        self.xkey=random.randint(0,self.width-30)
        self.ykey=random.randint(0,self.height-30)
        self.gotkey=False
        self.widthkey=25
        self.heightkey=30

        powerbox = pygame.image.load(r"game\images\power_box.png")
        self.powerbox = pygame.transform.scale(powerbox, (160, 200)) # This goes at (320, 180)

        self.deathText = pygame.image.load(r"game\images\death_text.png")
        self.deathText = pygame.transform.scale(self.deathText, (604, 480))
        self.prevangleis=0
        self.tentatives=40
        self.start=0
        self.waittimes=0

        battery = pygame.image.load(r"game\images\battery.png")
        self.battery_other = pygame.transform.scale(battery, (70, 52))
        self.battery_spawn = False
        self.pos = (random.randint(0, 520), random.randint(0, 400))
        self.c, self.d = self.pos[0], self.pos[1]

    def display(self,lighton,radius,clicked):
        self.screen.fill([0, 0, 0])
        self.clicked = clicked

        a, b = pygame.mouse.get_pos()
        self.a, self.b = a, b
        # put objects onto the background before calling array3d()
        if not self.gotkey:
            self.background.blit(self.key, (self.xkey, self.ykey))
            self.clickedkey(a,b)

        color = (255*self.used/self.battery, 255*(1-self.used/self.battery), 0)
        
        if self.battery_spawn:
            self.background.blit(self.battery_other, self.pos)
            if self.battery_spawn:
                if clicked:
                    self.clickedbattery(self.a, self.b, self.c, self.d)

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
            if self.clicked:
                self.gotkey=1
                self.background = pygame.image.load(r"game\images\first_room.png")
                self.background = pygame.transform.scale(self.background, (self.width, self.height))
                self.used /= 2
                self.battery_spawn = True
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

    def clickedbattery(self, a, b, c, d):
        if a>c and a<70+c and b>d and b<52+d:
            if self.clicked:
                self.battery_spawn = False
                self.used = 0
                self.background = pygame.image.load(r"game\images\first_room.png")
                self.background = pygame.transform.scale(self.background, (self.width, self.height))
                self.pos = (-100, -100)

    def why(self, start_ticks):
        self.seconds=(pygame.time.get_ticks()-start_ticks)/1000

        if int(ceil(self.seconds)) > self.previous_second:
                print(int(ceil(self.seconds)))
                self.previous_second = int(ceil(self.seconds))

                self.background = pygame.image.load(r"game\images\first_room.png")
                self.background = pygame.transform.scale(self.background, (self.width, self.height))

                self.screen.fill((0, 0, 0))

        self.time_text = self.font.render(f"{30-int(self.seconds)}", True, (255, 255, 255))
            
        self.time_left  = self.time_text.get_rect(center=(570, 40))
        self.screen.blit(self.time_text, self.time_left)
        self.background.blit(self.time_text, self.time_left)