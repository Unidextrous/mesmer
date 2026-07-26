from pathlib import Path

import moderngl
import numpy as np


class Renderer:
    def __init__(self, vertex_shader_path, fragment_shader_path, width, height):
        self.ctx = moderngl.create_context()

        self.width = width
        self.height = height

        self._create_quad()
        self._create_shader_program(
            vertex_shader_path,
            fragment_shader_path
        )

    def _create_quad(self):
        vertices = np.array([
            -1.0, -1.0,
             1.0, -1.0,
            -1.0,  1.0,

            -1.0,  1.0,
             1.0, -1.0,
             1.0,  1.0,
        ], dtype="f4")

        self.vbo = self.ctx.buffer(vertices.tobytes())

    def _create_shader_program(self, vertex_shader_path, fragment_shader_path):
        vertex_source = Path(vertex_shader_path).read_text()
        fragment_source = Path(fragment_shader_path).read_text()

        self.program = self.ctx.program(
            vertex_shader=vertex_source,
            fragment_shader=fragment_source,
        )

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, "2f", "in_position"),
            ],
        )

    def render(self, time, delta_time, frame):
        self.program["u_resolution"] = (self.width, self.height)

        self.vao.render()