import pygame

class Button():
    colour = (255, 255, 255)

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def show(self, win, text):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if text != '':
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                             self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True  
        return False


class Field(Button):
    baseColour = (23, 234, 134)
    visitedColour = ()
    wallColour = (234, 123, 23)

    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.walls = [True for _ in range(4)]#[up, down, left, right]
        self.visited = False

    def show(self, win):
        if self.visited:
            pygame.draw.rect(win, self.visitedColour, (self.x, self.y, self.width, self.height), 0)
        else:
            pygame.draw.rect(win, self.baseColour, (self.x, self.y, self.width, self.height), 0)

        if self.walls[0]:
            pygame.draw.line(win, self.wallColour, (self.x, self.y),
                                                 (self.x + self.width, self.y), 4)
        if self.walls[1]:
            pygame.draw.line(win, self.wallColour, (self.x, self.y + self.height),
                                                 (self.x + self.width, self.y + self.height), 4)
        if self.walls[2]:
            pygame.draw.line(win, self.wallColour, (self.x, self.y),
                                                 (self.x, self.y + self.height), 4)
        if self.walls[3]:
            pygame.draw.line(win, self.wallColour, (self.x + self.width, self.y),
                                                 (self.x + self.width, self.y + self.height), 4)