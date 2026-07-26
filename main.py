import pygame

from engine.renderer import Renderer


def main():
    pygame.init()

    pygame.display.set_mode(
        (0, 0),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN
    )

    renderer = Renderer(
        "shaders/vertex.vert",
        "shaders/fragment.frag",
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        renderer.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()