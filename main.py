import pygame

from engine.renderer import Renderer


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (0, 0),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN
    )

    width, height = screen.get_size()

    renderer = Renderer(
        "shaders/vertex.vert",
        "shaders/fragment.frag",
        width,
        height,
    )

    clock = pygame.time.Clock()
    elapsed_time = 0.0
    frame = 0

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    renderer.reload_shaders()

        delta_time = clock.tick(60) / 1000.0
        elapsed_time += delta_time

        renderer.render(elapsed_time, delta_time, frame)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()