import pygame

from engine.renderer import Renderer
from engine.visuals import VisualManager


def main():
    pygame.init()

    screen = pygame.display.set_mode(
        (0, 0),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN
    )

    width, height = screen.get_size()

    renderer = Renderer(width, height)

    visual_manager = VisualManager(renderer, "visuals", "visuals/default_vertex.vert")
    visual_manager.load("solid_color")

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
                elif event.key == pygame.K_1:
                    visual_manager.load("radial_gradient")
                elif event.key == pygame.K_2:
                    visual_manager.load("spiral")

        delta_time = clock.tick(60) / 1000.0
        elapsed_time += delta_time

        renderer.render(elapsed_time, delta_time, frame)
        renderer.check_shader_reload()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()