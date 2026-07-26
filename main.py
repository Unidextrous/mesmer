import pygame
import moderngl
import numpy as np

def main():
    pygame.init()

    pygame.display.set_mode(
        (1280, 720),
        pygame.OPENGL | pygame.DOUBLEBUF | pygame.FULLSCREEN
    )

    ctx = moderngl.create_context()

    with open("shaders/vertex.vert") as f:
        vertex_shader = f.read()

    with open("shaders/fragment.frag") as f:
        fragment_shader = f.read()

    program = ctx.program(
        vertex_shader=vertex_shader,
        fragment_shader=fragment_shader
    )

    vertices = np.array([
        -1.0, -1.0,
        1.0, -1.0,
        -1.0, 1.0,

        -1.0, 1.0,
        1.0, -1.0,
        1.0, 1.0
    ], dtype='f4')

    vbo = ctx.buffer(vertices.tobytes())

    vao = ctx.vertex_array(
        program,
        [
            (vbo, '2f', 'in_position')
        ],
    )

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
    
        vao.render()
        
        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()