import pygame

from engine.renderer import Renderer
from engine.visuals import VisualManager


def load_preset(renderer, preset_name):
    visual_name = renderer.current_visual_instance.visual.name

    preset_path = (
        f"visuals/{visual_name}/presets/{preset_name}.toml"
    )

    print(preset_path)

    renderer.current_visual_instance.parameter_manager.load_preset(
        preset_path
    )

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
                    visual_manager.load_next(
                        "solid_color",
                        "visuals/solid_color/presets/default.toml"
                    )
                    renderer.iris.start(direction=1)
                elif event.key == pygame.K_4:
                    visual_manager.load_next(
                        "ripple",
                        "visuals/ripple/presets/light.toml"
                    )
                    renderer.iris.start(direction=0)
                elif event.key == pygame.K_5:
                    load_preset(renderer, "default")
                elif event.key == pygame.K_6:
                    load_preset(renderer, "light")
                elif event.key == pygame.K_7:
                    load_preset(renderer, "dark")

        delta_time = clock.tick(60) / 1000.0
        elapsed_time += delta_time

        renderer.render(elapsed_time, delta_time, frame)

        pygame.display.flip()

        frame += 1

    pygame.quit()


if __name__ == "__main__":
    main()