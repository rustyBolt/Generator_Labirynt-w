def main():
    import pygame
    import src.maze as maze

    white = (255, 255, 255)
    mazeX = 20
    mazeY = 20
    maxMazeWidth = 600
    add = lambda x: x + 1
    subtract = lambda x: x - 1
    m = []
    clickers = []
    points = []
    R = 0
    C = 0

    pygame.init()

    display = pygame.display.set_mode((900, 700))

    Rows = maze.Stat(630, 20, 100, 50)
    Collumns = maze.Stat(630, 130, 100, 50)
    changers = [maze.StatChange(630, 70, 50, "+", Rows, add),
                maze.StatChange(680, 70, 50, "-", Rows, subtract),
                maze.StatChange(630, 180, 50, "+", Collumns, add),
                maze.StatChange(680, 180, 50, "-", Collumns, subtract)]

    Generate = maze.Button(630, 250, 200, 50, "Generój")

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
                        R = Rows.get()
                        C = Collumns.get()

                        if R>0 and C>0:
                            if C > R:
                                L = C
                            else:
                                L = R

                            clickers = maze.generateClickers(mazeX, mazeY, maxMazeWidth//L, R, C)

                if Generate.isOver(pos):
                    clickers = []
                    grid = maze.generateGrid(R, C, points[0], points[1])
                    m = maze.fillMaze(mazeX, mazeY, maxMazeWidth//L, grid)

                for i in clickers:
                    if i.isOver(pos):
                        a = i.action()

                        if a in points:
                            points.remove(a)
                        elif not points:
                            points.append(a)
                        elif len(points) == 1:
                            points.append(a)
                        
                        
                        print(points)

        display.fill(white)

        Rows.show(display)
        Collumns.show(display)
        Generate.show(display)
        for i in changers:
            i.show(display)

        maze.drawClickers(display, clickers)

        maze.drawMaze(display, m)

        pygame.display.update()


if __name__ == '__main__':
    main()