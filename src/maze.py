import pygame
import random
import math

minDim = 2
maxDim = 30

class InvalidDimensionsError(Exception):
    '''
    Zwracany jest gdy podane zostaną niewłaściwe wymiary.

    Przyjmuje tekst jaki będzie wypisany 
    jako doprecyzowanie co się stało.
    '''
    def __init__(self, text):
        self.text = text

class InvalidPositionError(Exception):
    '''
    Zwracany jest gdy podane zostaną niewłaściwe punkty.

    Przyjmuje tekst jaki będzie wypisany 
    jako doprecyzowanie co się stało.
    '''
    def __init__(self, text):
        self.text = text

class Button():
    '''
    Prosty przycisk.
    
    Metoda action() jest wirtualna do sprecyzowania póżniej.
    '''
    colour = (255, 255, 0)

    def __init__(self, x, y, width, height, text):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    #Rysuje przycisk na ekranie
    def show(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y,
                                     self.width, self.height), 0)

        if self.text:
            font = pygame.font.SysFont('comicsans', 60)
            text = font.render(self.text, 1, (0,0,0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2),
                             self.y + (self.height/2 - text.get_height()/2)))

    #Sprawdza czy kliknięto w przcisk
    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True  
        return False

    #Określa co stanie się po kliknięciu
    def action(self):
        pass

class Stat(Button):
    '''
    Przechowuje numer i wyświetla go na ekranie.
    '''
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
    '''
    Zmienia wartość przypisanego do siebie obiektu.

    Przyjmuje obiekt (w tym programie) Stat i 
    manipuluje jego wartościami.
    '''
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

class Wall(Button):
    '''Ściana labiryntu.'''
    colour = (0, 0, 0)

    def __init__(self, x, y, length):
        self.x = x
        self.y = y
        self.width = length
        self.height = length

    def show(self, win):
        pygame.draw.rect(win, self.colour, (self.x, self.y,
                                     self.width, self.height), 0)

class Clicker(Wall):
    '''
    Służy do wybierania punktów startowego i końcowego.
    
    Po kliknięciu zwraca swoją pozycję i zmienia kolor.
    '''
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

        pygame.draw.rect(win, colour, (self.x, self.y,
                                         self.width, self.height), 0)

    def action(self):
        if self.clicked:
            self.clicked = False
        else:
            self.clicked = True

        return self.point

class Corridor(Clicker):
    '''
    Korytarz labiryntu.
    
    Po kliknięciu zwraca swoją pozycję i zmienia kolor.
    '''
    baseColour = (23, 234, 134)
    visitedColour = (234, 123, 23)
    cColour = (255, 0, 0)

    def __init__(self, x, y, length, point):
        self.x = x
        self.y = y
        self.width = length
        self.height = length
        self.clicked = False
        self.point = point
        self.visited = False
        self.special = False

    def show(self, win):
        if self.special:
            colour = self.cColour
        elif self.clicked:
            colour = self.cColour
        elif self.visited:
            colour = self.visitedColour
        else:
            colour = self.baseColour

        pygame.draw.rect(win, colour, (self.x, self.y,
                                 self.width, self.height), 0)

def generateGrid(amountR, amountC, start, end):
    '''
    Generuje listę punktów będącą reprezentacją labiryntu .

    Zwraca listę dwuwymiarową wypełnioną 0 i 1 odpowiadającym 
    ścianom i korytarzom labiryntu o podanych rozmiarach od 
    punktu startowego do końcowego.

    Po podaniu niewłaściwych punktów startu i końca lub 
    gdy podane wielkości są za duże bądź za małe zwraca błąd.
    '''
    if amountC < minDim or amountR < minDim:
        raise InvalidDimensionsError(
            "Za małe wymiary!"
        )

    if amountC > maxDim or amountR  > maxDim:
        raise InvalidDimensionsError(
            "Za duże wymiary!"
        )

    if not start or not end\
        or start == end:
        raise InvalidPositionError(
            "Nie wybrano punktów"
        )

    maze = [[0 for _ in range(amountC)] for _ in range(amountR)]
    stack = []
    d = 0
    found = False

    direction = [(start[0]+1, start[1]),
                  (start[0], start[1]+1),
                  (start[0]-1, start[1]),
                  (start[0], start[1]-1)]

    directions = direction.copy()

    for i in direction:
        if i[0] < 0 or i[0] > amountR - 1 or\
                 i[1] < 0 or i[1] > amountC - 1:
            index = directions.index(i)
            del directions[index]

    x = abs(start[0] - end[0])
    y = abs(start[1] - end[1])

    if x == 0 or y == 0:
        distance = amountR + amountC
        chosen = ()

        for i in directions:
            dist = math.sqrt(
                (i[0] - end[0])**2 + (i[1] - end[1])**2)
            if distance > dist:
                distance = dist
                chosen = i

        index = directions.index(chosen)
        del directions[index]

    stack.append([start, directions])
    maze[start[0]][start[1]] = 1

    areaR = amountR // 2
    areaC = amountC // 2

    #Wykorzystany algorytm to algorytm przeszukiwania z krokiem 3
    while stack:
        current = stack[-1]

        if current[0] == end:
            maze[current[0][0]][current[0][1]] = 1
            del stack[-1]
            d = 0
            found = True
            continue

        if current[1]:
            next = ()
            if not found:
                #Sprawdza czy głowa przeszukiwacza znajduje sie w 
                #Otoczeniu punktu końcowego
                if areaR > end[0]:
                    if current[0][0] >= end[0]\
                        and  current[0][0] <= areaR:
                        isR = True
                    else:
                        isR = False
                else:
                    if current[0][0] >= areaR\
                        and  current[0][0] <= end[0]:
                        isR = True
                    else:
                        isR = False

                if areaC > end[1]:
                    if current[0][1] >= end[1]\
                        and  current[0][1] <= areaC:
                        isC = True
                    else:
                        isC = False
                else:
                    if current[0][1] >= areaC\
                        and  current[0][1] <= end[1]:
                        isC = True
                    else:
                        isC = False
                
                #Jeśli tak kiruje glowę do punktu końcowego
                if isC and isR:
                    d = 0
                    distance = amountC + amountR
                    chosen = ()
                    for i in current[1]:
                        dist = math.sqrt(
                            (i[0] - end[0])**2 + (i[1] - end[1])**2)
                        if distance > dist:
                            distance = dist
                            chosen = i
                    
                    next = chosen
                    current[1].remove(next)

            if not next:
                #Przeszukuje labirynt z krokiem 3
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

                        if not next:
                            next = random.choice(current[1])
                            current[1].remove(next)

                else:
                    next = random.choice(current[1])
                    current[1].remove(next)

            if not next:
                next = current[1][0]
                current[1].remove(next)

            #Wybiera, które punkty będą następne
            direction = [(next[0]+1, next[1]),
                          (next[0], next[1]+1),
                          (next[0]-1, next[1]),
                          (next[0], next[1]-1)]

            directions = direction.copy()
                
            for i in directions:
                if i[0] < 0 or i[0] > amountR-1 or\
                             i[1] < 0 or i[1] > amountC-1:
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

    maze[end[0]][end[1]] = 1

    return maze

def createPath(grid, start, end, amountR, amountC):
    '''
    Generuje ścierzkę między punktem startowym i końcowym.

    Zwraca listę punktów między punktem startowym i końcowym 
    dla podanej siatki punktów.

    Gdy podane wielkości są za duże bądź za małe 
    lub gdy podana siatka jest pusta zwraca błąd.
    '''

    if amountC < minDim or amountR < minDim:
        raise InvalidDimensionsError(
            "Za małe wymiary!"
        )

    if amountC > maxDim or amountR  > maxDim:
        raise InvalidDimensionsError(
            "Za duże wymiary!"
        )

    if not grid:
        raise InvalidDimensionsError(
            "Złe wymiary!"
        )

    stack = []

    directions = [(start[0]+1, start[1]),
                  (start[0], start[1]+1),
                  (start[0]-1, start[1]),
                  (start[0], start[1]-1)]

    for i in directions:
        if i[0] < 0 or i[0] > amountR - 1 or\
                     i[1] < 0 or i[1] > amountC - 1:
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

    #Wykorzystuje algorytm przeszukiwania 
    #Zawsze wybiera punkt najbliżej punktu końcowego
    while stack:
        current = stack[-1]

        if current[0] == end:
            break

        if current[1]:
            distance = amountR + amountC
            next = ()
            for i in current[1]:
                dist = math.sqrt((i[0] - end[0])**2 + (i[1] - end[1])**2)
                if dist < distance:
                    distance = dist
                    next = i

            current[1].remove(next)

            direction = [(next[0]+1, next[1]),
                          (next[0], next[1]+1),
                          (next[0]-1, next[1]),
                          (next[0], next[1]-1)]

            directions = direction.copy()
                
            for i in directions:
                if i[0] < 0 or i[0] > amountR-1\
                             or i[1] < 0 or i[1] > amountC-1:
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

def createMultiplePath(grid, start, end, points, amountR, amountC):
    '''
    Generuje ścierzkę między punktem startowym i końcowym 
    poprzez podane punkty pośrednie.

    Zwraca listę punktów między punktem startowym i końcowym 
    dla podanej siatki punktów.

    Gdy podane wielkości są za duże bądź za małe 
    lub gdy podana siatka jest pusta zwraca błąd.
    '''

    if amountC < minDim or amountR < minDim:
        raise InvalidDimensionsError(
            "Za małe wymiary!"
        )

    if amountC > maxDim or amountR  > maxDim:
        raise InvalidDimensionsError(
            "Za duże wymiary!"
        )

    if not grid:
        raise InvalidDimensionsError(
            "Złe wymiary!"
        )

    points.insert(0, start)
    points.append(end)
    paths = []

    try:
        for i in range(len(points)):
            p = createPath(grid, points[i],
                         points[i + 1], amountR, amountC)
            paths = paths + p
    except IndexError:
        return paths

def fillMaze(X, Y, length, grid):
    '''
    Wypełnia siatkę punktów korytarzami i ścianami.
    
    Zwraca liste wypełnioną obiektami ścian i korytarzy 
    o podanej szerokości zaczynając od podanych współrzędnych.
    '''
    x = X
    y = Y
    maze = []

    if grid:
        for i in range(len(grid)):
            row = []
            for j in range(len(grid[0])):
                if grid[i][j] == 1:
                    row.append(Corridor(x, y, length, (i, j)))
                else:
                    row.append(Wall(x, y, length))

                x = x + length
            maze.append(row)
            y = y + length
            x = X

    return maze   

def generateClickers(X, Y, length, Rows, Collumns):
    '''Tworzy przyciski do wybierana punktów startowego i końcowego.'''
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
    '''Koloruje ścierzkę w labiryncie.'''
    if maze:
        for i in range(len(maze)):
            for j in range(len(maze[0])):
                if (i, j) in path:
                    maze[i][j].visited = True
                else:
                    maze[i][j].visited = False

def drawMaze(win, grid):
    '''Rysuje labirynt na ekranie.'''
    for i in grid:
        for j in i:
            j.show(win)

def drawClickers(win, l):
    '''Rysje na ekranie przyciski do wybierania punktów.'''
    for i in l:
        i.show(win)

def showSpecial(grid, points):
    '''Koloruje start i koniec.'''
    for i in points:
        grid[i[0]][i[1]].special = True