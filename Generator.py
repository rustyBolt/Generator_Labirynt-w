def main():
    import pygame
    import src.maze as maze

    white = (255, 255, 255)
    mazeX = 20
    mazeY = 20
    maxMazeWidth = 600

    pygame.init()

    display = pygame.display.set_mode((800, 600))
    display.fill(white)

    R = 30
    C = 30
    grid = maze.generateGrid(mazeX, mazeY, maxMazeWidth//C, R, C, (3, 0), ())
    #Rows = maze.Stat(610, 20, 30, 20)
    #buttons = [Rows, maze.StatIncrement()]

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        maze.drawMaze(display, grid)

        pygame.display.update()

if __name__ == '__main__':
    main()