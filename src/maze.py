import pygame
import random

class Button():
    colour = (255, 255, 0)

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

class StatChange(Button):
    def __init__(self, x, y, length, text, object, function):
        self.x = x
        self.y = y
        self.width = length
        self.height = length
        self.text = text
        self.object = object
        self.function = function

    def action(self):
        x = self.function(self.object.get())
        self.object.set(x)

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
    colour = (0, 0, 0)

    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.width = length
        self.height = length

    def show(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y, self.width, self.height), 0)

class Clicker(Wall):
    clickedColour = (255, 0, 0)
    def __init__(self, x, y, length, point):
        self.x = x
        self.y = y
        self.width = length
        self.height = length
        self.clicked = False
        self.point = point
    
    def show(self, win):
        if self.clicked:
            colour = self.clickedColour
        else:
            colour = self.colour

        pygame.draw.rect(win, colour, (self.x, self.y, self.width, self.height), 0)

    def action(self):
        if self.clicked:
            self.clicked = False
        else:
            self.clicked = True

        return self.point

def generateGrid(amountR, amountC, start, end):
    maze = [[0 for _ in range(amountC)] for _ in range(amountR)]
    stack = []
    d = 0
    vertical = False

    if end[1] == amountC -1:
        end2 = (end[0], end[1] - 1)
        vertical = True
    if end[1] == 0:
        end2 = (end[0], end[1] + 1)
        vertical = True
    if end[0] == amountR -1:
        end2 = (end[0] - 1, end[1])
    if end[0] == 0:
        end2 = (end[0] + 1, end[1])

    directions = [(start[0]+1, start[1]),
                  (start[0], start[1]+1),
                  (start[0]-1, start[1]),
                  (start[0], start[1]-1)]

    for i in directions:
        if i[0] < 0 or i[0] > amountR - 1 or i[1] < 0 or i[1] > amountC - 1:
            index = directions.index(i)
            del directions[index]

    stack.append([start, directions])
    maze[start[0]][start[1]] = 1
    maze[end[0]][end[1]] = 1
    maze[end2[0]][end2[1]] = 1

    while stack:
        current = stack[-1]

        if current[1]:
            if d%3 == 0:
                d = 0

            if d > 0:
                if len(stack) > 1:
                    before = stack[-2][0]

                a = [-1, -1]
                c = current[0]

                if c[0] == before[0]:
                    a[0] = c[0]
                elif c[1] == before[1]:
                    a[1] = c[1]

                if a[0] > -1:
                    a[0], a[1] = 0, a[0]
                else:
                    a[0] = 1

                for i in current[1]:
                    if i[a[0]] == a[1]:
                        next = i
                        current[1].remove(next)
            else:
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

            d = d + 1

        else:
            del stack[-1]
            d = 0

    if vertical:
        found = False

        if not found:
            if end2[0] > 1 :
                if maze[end2[0] - 2][end2[1]] == 1:
                    if not maze[end2[0] - 1][end2[1] - 1] == 1\
                        or maze[end2[0] - 1][end2[1] + 1] == 1:
                        maze[end2[0] - 1][end2[1]] = 1
                        found = True
        if not found:
            if end2[0] < amountR -2:
                if maze[end2[0] + 2][end2[1]] == 1:
                    if not maze[end2[0] + 1][end2[1] + 1] == 1\
                        or maze[end2[0] + 1][end2[1] - 1] == 1:
                        maze[end2[0] + 1][end2[1]] = 1
                        found = True
        if not found:
            if end[0] > 1 :
                if maze[end[0] - 2][end[1]] == 1:
                    maze[end[0] - 1][end[1]] = 1
                    found = True
        if not found:
            if end[0] < amountR -2:
                if maze[end[0] + 2][end[1]] == 1:
                    maze[end[0] + 1][end[1]] = 1
                    found = True
    else:
        found = False

        if not found:
            if end2[1] > 1:
                if maze[end2[0]][end2[1] - 2] == 1:
                    if not maze[end2[0] + 1][end2[1] - 1] == 1\
                        or maze[end2[0] - 1][end2[1] - 1] == 1:
                        maze[end2[0]][end2[1] - 1] = 1
                        found = True
        if not found:
            if end2[1] < amountC - 2:
                if maze[end2[0]][end2[1] + 2] == 1:
                    if not maze[end2[0] + 1][end2[1] + 1] == 1\
                        or maze[end2[0] - 1][end2[1] + 1] == 1:
                        maze[end2[0]][end2[1] + 1] = 1
                        found = True
        if not found:
            if end[1] > 1:
                if maze[end[0]][end[1] - 2] == 1:
                    maze[end[0]][end[1] - 1] = 1
                    found = True
        if not found:
            if end[1] < amountC - 2:
                if maze[end[0]][end[1] + 2] == 1:
                    maze[end[0]][end[1] + 1] = 1
                    found = True

    maze[start[0]][start[1]] = 1

    return maze

def createPath(grid, start, end, amountR, amountC):
    stack = []

    directions = [(start[0]+1, start[1]),
                  (start[0], start[1]+1),
                  (start[0]-1, start[1]),
                  (start[0], start[1]-1)]

    for i in directions:
        if i[0] < 0 or i[0] > amountR - 1 or i[1] < 0 or i[1] > amountC - 1:
            index = directions.index(i)
            del directions[index]

    for i in directions:
        if grid[i[0]][i[1]] == 0:
            index = directions.index(i)
            del directions[index]

    dir = []

    for i in directions:
        if grid[i[0]][i[1]] == 1:
            dir.append(i)

    stack.append([start, dir])

    while stack:
        current = stack[-1]

        if current[0] == end:
            break

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

            dir = []

            for i in direction:
                if grid[i[0]][i[1]] == 1:
                    dir.append(i)

            stack.append([next, dir])

        else:
            del stack[-1]

    path = []

    for i in stack:
        path.append(i[0])

    return path


def fillMaze(X, Y, length, grid):
    x = X
    y = Y
    maze = []

    for i in grid:
        row = []
        for j in i:
            if j == 1:
                row.append(Corridor(x, y, length))
            else:
                row.append(Wall(x, y, length))

            x = x + length
        maze.append(row)
        y = y + length
        x = X

    return maze   

def generateClickers(X, Y, length, Rows, Collumns):
    x = X
    y = Y
    clickers = []

    for i in range(Rows):
        for j in range(Collumns):
            if i == 0 or i == Rows - 1\
                or j == 0 or j == Collumns - 1:
                    clickers.append(Clicker(x, y, length, (i, j)))
            x = x + length
        y = y + length
        x = X

    return clickers

def drawPath(maze, path):
    for i in range(len(maze)):
        for j in range(len(maze[0])):
            if (i, j) in path:
                maze[i][j].visited = True

def drawMaze(win, grid):
    for i in grid:
        for j in i:
            j.show(win)

def drawClickers(win, l):
    for i in l:
        i.show(win)