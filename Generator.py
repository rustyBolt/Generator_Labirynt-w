def main():
    import pygame

    pygame.init()

    white = (255, 255, 255)

    display = pygame.display.set_mode((800, 600))
    display.fill(white)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

if __name__ == '__main__':
    main()