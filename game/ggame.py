import sys
import pygame
from game.screens.title import TitleScreen
from game.screens.spaceship import GameScreen
from pygame import gfxdraw, mixer
import numpy as np
from mpmath import *
from game.screens.displayhelp import DisplayHelp

mixer.init()
mixer.Channel(1).set_volume(0.2)

class Game:
    def __init__(self, width=604, height=480, caption="Space Repair"):
        pygame.init()
        pygame.display.set_caption(caption)
        self.window_size=[width, height]
        self.screen = pygame.display.set_mode(self.window_size)
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 50)
        self.frames = 0
        self.previous_second = 0

        self.dh = DisplayHelp()
        self.help = 0

        self.title_screen = TitleScreen(width, height)
        self.game_screen=GameScreen(width,height)
        self.is_playing = False
        self.lighton=1
        self.radius=30
        self.clicked=0
    def run(self):
        self.start_ticks = 0
        while True:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()
            if self.is_playing:
                if self.start_ticks == 0:
                    self.start_ticks = pygame.time.get_ticks()

                self.game_screen.why(self.start_ticks)

            self.game_screen.get_keys(self.keys)

    def handle_events(self):
        for event in pygame.event.get():
            self.keys = pygame.key.get_pressed()
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key==pygame.K_h:
                    self.help=1-self.help
                elif event.key == pygame.K_SPACE:
                    self.is_playing=1-self.is_playing
                    self.screen.fill((0, 0, 0))
                elif event.key==pygame.K_f:
                    self.lighton=1-self.lighton
                    mixer.Channel(1).play(mixer.Sound(r"game\sounds\flashlight.mp3"))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button==4 or event.button==5:
                    if event.button == 4 and self.radius<80:
                        self.radius +=5
                    if event.button == 5 and self.radius>10 :
                        self.radius-=5
                if event.button==1:
                    self.clicked=1
            else:
                self.clicked=0
    def update(self):
        pass

    def draw(self):
        if self.help:
            self.dh.display()
        elif self.is_playing:
            self.game_screen.display(self.lighton, self.radius, self.clicked)
        else:
            self.title_screen.display()

        pygame.display.flip()
