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

    visual_manager = VisualManager(
        renderer,
        "visuals",
        "visuals/default_vertex.vert"
    )

    visual_manager.load("spiral")

    visual_manager.load_next(
        "spiral",
        "visuals/spiral/presets/reverse.toml"
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
                    renderer.current_visual_instance.reload_shaders()
                    renderer.next_visual_instance.reload_shaders()
                elif event.key == pygame.K_1:
                    visual_manager.load_next(
                        "spiral",
                        "visuals/spiral/presets/default.toml"
                    )
                    renderer.iris.start(direction=0)
                elif event.key == pygame.K_2:
                    visual_manager.load_next(
                        "spiral",
                        "visuals/spiral/presets/reverse.toml"
                    )
                    renderer.iris.start(direction=0)
                elif event.key == pygame.K_3:
                    renderer.current_visual_instance.parameter_manager.load_preset(
                        "visuals/spiral/presets/default.toml"
                    )
                elif event.key == pygame.K_4:
                    renderer.current_visual_instance.parameter_manager.load_preset(
                        "visuals/spiral/presets/light.toml"
                    )
                elif event.key == pygame.K_5:
                    renderer.current_visual_instance.parameter_manager.load_preset(
                        "visuals/spiral/presets/dark.toml"
                    )

        delta_time = clock.tick(60) / 1000.0
        elapsed_time += delta_time

        renderer.render(elapsed_time, delta_time, frame)

        pygame.display.flip()

        frame += 1

    pygame.quit()


if __name__ == "__main__":
    main()