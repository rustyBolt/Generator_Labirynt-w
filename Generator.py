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

    pygame.init()

    display = pygame.display.set_mode((800, 800))

    Rows = maze.Stat(630, 20, 100, 50)
    Radd = maze.StatChange(630, 70, 50, "+", Rows, add)
    Rsub = maze.StatChange(680, 70, 50, "-", Rows, subtract)
    Collumns = maze.Stat(630, 130, 100, 50)
    Cadd = maze.StatChange(630, 180, 50, "+", Collumns, add)
    Csub = maze.StatChange(680, 180, 50, "-", Collumns, subtract)

    Generate = maze.Button(630, 250, 200, 50, "Generój")

    while True:
        display.fill(white)

        Rows.show(display)
        Collumns.show(display)
        Generate.show(display)
        Radd.show(display)
        Rsub.show(display)
        Cadd.show(display)
        Csub.show(display)

        R = Rows.get()
        C = Collumns.get()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                if Radd.isOver(pos):
                    Radd.action()

                if Rsub.isOver(pos):
                    Rsub.action()

                if Cadd.isOver(pos):
                    Cadd.action()

                if Csub.isOver(pos):
                    Csub.action()

                if Generate.isOver(pos):
                    grid = maze.generateGrid(R, C, (3, 0), ())
                    m = maze.fillMaze(mazeX, mazeY, maxMazeWidth//C, grid)


        maze.drawMaze(display, m )

        pygame.display.update()


if __name__ == '__main__':
    main()