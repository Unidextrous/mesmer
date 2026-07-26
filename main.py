import pygame


def main():
    pygame.init()

    pygame.display.set_mode(
        (1280, 720),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()