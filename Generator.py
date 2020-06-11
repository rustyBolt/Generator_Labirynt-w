def main():
    import pygame
    import src.maze as maze

    white = (255, 255, 255)
    mazeX = 20
    mazeY = 20
    maxMazeWidth = 600
    peekX = 630
    peekY = 240
    maxPeekWidth = 300
    m = []
    peek = []
    clickers = []
    points = []
    multiple = []
    path = []
    R = 0
    C = 0
    add = lambda x: x + 1
    subtract = lambda x: x - 1

    pygame.init()

    display = pygame.display.set_mode((1100, 700))

    Rows = maze.Stat(630, 20, 100, 50)
    Collumns = maze.Stat(630, 130, 100, 50)
    changers = [maze.StatChange(630, 70, 50, "+", Rows, add),
                maze.StatChange(680, 70, 50, "-", Rows, subtract),
                maze.StatChange(630, 180, 50, "+", Collumns, add),
                maze.StatChange(680, 180, 50, "-", Collumns, subtract)]

    Generate = maze.Button(745, 20, 200, 50, "Generój")
    Reset = maze.Button(745, 85, 200, 50, "Wyczyść")

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                for i in changers:
                    if i.isOver(pos):
                        i.action()
                        peek = []
                        points = []
                        R = Rows.get()
                        C = Collumns.get()

                        if R>0 and C>0:
                            if C > R:
                                L = C
                            else:
                                L = R

                            clickers = maze.generateClickers(mazeX, mazeY, maxMazeWidth//L, R, C)

                for i in clickers:
                    if i.isOver(pos):
                        a = i.action()

                        if a in points:
                            points.remove(a)
                        elif not points:
                            points.append(a)
                        elif len(points) == 1:
                            points.append(a)
                            
                        if len(points) == 2:
                            grid = maze.generateGrid(R, C, points[0], points[1])
                            peek = maze.fillMaze(peekX, peekY, maxPeekWidth//L, grid)
                        else:
                            grid = []
                            peek = []

                if Generate.isOver(pos):
                    clickers = []
                    peek = []
                    path = maze.createPath(grid, points[0], points[1], R, C)
                    m = maze.fillMaze(mazeX, mazeY, maxMazeWidth//L, grid)
                    maze.drawPath(m, path)

                if Reset.isOver(pos):
                    if m:
                        path = []
                        m = []
                        multiple = []
                        points = []
                        peek = []

                        clickers = maze.generateClickers(mazeX, mazeY, maxMazeWidth//L, R, C)

                for i in m:
                    for j in i:
                        if j.isOver(pos):
                            p = j.action()

                            if not p is None:
                                if p in multiple:
                                    multiple.remove(p)
                                else:
                                    multiple.append(p)
                            
                            if multiple:
                                paths = maze.createMultiplePath(
                                    grid, points[0], points[1], multiple, R, C)

                                maze.drawPath(m, paths)

                            else:
                                maze.drawPath(m, path)

        display.fill(white)

        Rows.show(display)
        Collumns.show(display)
        Generate.show(display)
        Reset.show(display)
        for i in changers:
            i.show(display)

        maze.drawClickers(display, clickers)

        maze.drawMaze(display, m)
        maze.drawMaze(display, peek)

        pygame.display.update()


if __name__ == '__main__':
    main()