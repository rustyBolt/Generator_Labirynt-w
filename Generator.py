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
    grid = []
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
    Error = maze.Button(20, 650, 600, 50, "")

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

                        if R>maze.minDim and C>maze.minDim\
                            and R <= maze.maxDim and C <= maze.maxDim:
                            if C > R:
                                L = C
                            else:
                                L = R

                            clickers = maze.generateClickers(mazeX, mazeY,
                                                     maxMazeWidth//L, R, C)
                        else:
                            clickers = []

                        Error = maze.Button(20, 650, 600, 50, "")

                for i in clickers:
                    if i.isOver(pos):
                        Error = maze.Button(20, 650, 600, 50, "")

                        a = i.action()

                        if a in points:
                            points.remove(a)
                        else:
                            points.append(a)

                        if len(points) > 2:
                            a = i.action()
                            points.remove(a)
                            
                        if len(points) == 2:
                            try:
                                if abs(points[0][0] - points[1][0])\
                                    + abs(points[0][1] - points[1][1])\
                                        == 1:
                                    a = i.action()
                                    points.remove(a)
                                    raise maze.InvalidPositionError(
                                        "Punkty nie mogą być obok siebie!"
                                    )

                                grid = maze.generateGrid(R, C, 
                                                points[0], points[1])
                                peek = maze.fillMaze(peekX, peekY,
                                             maxPeekWidth//L, grid)
                                maze.showSpecial(peek, points)
                            except maze.InvalidDimensionsError as e:
                                Error = maze.Button(20, 650, 600, 50,
                                             e.text)
                            except maze.InvalidPositionError as e:
                                Error = maze.Button(20, 650, 600, 50,
                                             e.text)
                        else:
                            grid = []
                            peek = []

                if Generate.isOver(pos):
                    try:
                        if R < maze.minDim or C < maze.minDim:
                            raise maze.InvalidDimensionsError(
                            "Za małe wymiary!"
                            )

                        if R > maze.maxDim or C > maze.maxDim:
                            raise maze.InvalidDimensionsError(
                            "Za duże wymiary!"
                            )

                        if len(points) < 2 or not grid:
                            raise maze.InvalidPositionError(
                            "Nie wybrano punktów")

                        clickers = []
                        peek = []
                        path = maze.createPath(grid, 
                                    points[0], points[1], R, C)
                        m = maze.fillMaze(mazeX, mazeY,
                                            maxMazeWidth//L, grid)
                        maze.drawPath(m, path)
                        maze.showSpecial(m, points)
                    except maze.InvalidDimensionsError as e:
                        Error = maze.Button(20, 650, 600, 50,
                                             e.text)
                    except maze.InvalidPositionError as e:
                        Error = maze.Button(20, 650, 600, 50,
                                             e.text)
                    else:
                        Error = maze.Button(20, 650, 600, 50,
                                             "")

                if Reset.isOver(pos):
                    if m:
                        path = []
                        m = []
                        multiple = []
                        points = []
                        peek = []

                        clickers = maze.generateClickers(mazeX,
                                     mazeY, maxMazeWidth//L, R, C)

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
                                    grid, points[0], points[1],
                                                     multiple, R, C)

                                maze.drawPath(m, paths)

                            else:
                                maze.drawPath(m, path)

        display.fill(white)

        Rows.show(display)
        Collumns.show(display)
        Generate.show(display)
        Error.show(display)
        Reset.show(display)
        for i in changers:
            i.show(display)

        maze.drawClickers(display, clickers)

        maze.drawMaze(display, m)
        maze.drawMaze(display, peek)

        pygame.display.update()


if __name__ == '__main__':
    main()