import pygame

class DisplayHelp:
    def init(self, width, height):
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((self.width, self.height))
        self.font = pygame.font.Font(None, 50)



        self.bg_pic = pygame.image.load(r"game\images\how_to_play.png")
        self.bg_pic = pygame.transform.scale(self.bg_pic, (self.width, self.height))
    def display(self):

        self.bg_rect = self.bg_pic.get_rect(center=(self.width//2, self.height//2))

        self.screen.blit(self.bg_pic, self.bg_rect)