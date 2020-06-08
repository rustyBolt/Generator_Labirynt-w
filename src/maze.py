import pygame
import random

class Button():
    colour = (255, 255, 255)

    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def show(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

        if self.text:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                             self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True  
        return False

    def action(self):
        pass

class Stat(Button):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = '0'
        self.value = 0

    def get(self):
        return self.value

    def set(self, newV):
        self.value = newV
        self.text = str(newV)

class StatIncrement(Button):
    def __init__(self, x, y, length, text, object):
        self.x = x
        self.y = y
        self.width = length
        self.height = length
        self.text = '+'
        self.object = object

    def action(self):
        self.object.set(self.object.get() + 1)

class StatDecrement(Button):
    def __init__(self, x, y, length, text, object):
        self.x = x
        self.y = y
        self.width = length
        self.height = length
        self.text = '-'
        self.object = object

    def action(self):
        self.object.set(self.object.get() - 1)

class Corridor(Button):
    baseColour = (23, 234, 134)
    visitedColour = (234, 123, 23)

    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.width = length
        self.height = length
        self.visited = False

    def show(self, win):
        if self.visited:
            colour = self.visitedColour
        else:
            colour = self.baseColour

        pygame.draw.rect(win, colour, (self.x, self.y, self.width, self.height), 0)

class Wall(Button):
    wallColour = (0, 0, 0)

    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.width = length
        self.height = length

    def show(self, win):
        pygame.draw.rect(win, self.wallColour, (self.x, self.y, self.width, self.height), 0)

def generateGrid(X, Y, length, amountR, amountC, start, end):
    grid = []
    maze = [[0 for _ in range(amountC)] for _ in range(amountR)]
    stack = []

    directions = [(start[0]+1, start[1]),
                  (start[0], start[1]+1),
                  (start[0]-1, start[1]),
                  (start[0], start[1]-1)]

    for i in directions:
        if i[0] < 0 or i[0] > amountR or i[1] < 0 or i[1] > amountC:
            index = directions.index(i)
            del directions[index]

    stack.append([start, directions])
    maze[start[0]][start[1]] = 1

    while stack:
        current = stack[-1]

        if current[1]:
            next = random.choice(current[1])
            current[1].remove(next)

            direction = [(next[0]+1, next[1]),
                          (next[0], next[1]+1),
                          (next[0]-1, next[1]),
                          (next[0], next[1]-1)]

            directions = direction.copy()
                
            for i in directions:
                if i[0] < 0 or i[0] > amountR-1 or i[1] < 0 or i[1] > amountC-1:
                    index = direction.index(i)
                    del direction[index]

                if i == current[0]:
                    index = direction.index(i)
                    del direction[index]

            for i in direction:
                if maze[i[0]][i[1]] == 1:
                    break
            else:
                stack.append([next, direction])
                maze[next[0]][next[1]] = 1

        else:
            del stack[-1]

    x = X
    y = Y
    for i in maze:
        row = []
        for j in i:
            if j == 1:
                row.append(Corridor(x, y, length))
            else:
                row.append(Wall(x, y, length))

            x = x + length
        grid.append(row)
        y = y + length
        x = X

    return grid

def drawMaze(win, grid):
    for i in grid:
        for j in i:
            j.show(win)