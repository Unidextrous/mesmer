from pathlib import Path

import moderngl
import numpy as np


class Renderer:
    def __init__(self, vertex_shader_path, fragment_shader_path, width, height):
        self.ctx = moderngl.create_context()

        self.width = width
        self.height = height

        self.vertex_shader_path = vertex_shader_path
        self.fragment_shader_path = fragment_shader_path

        self._create_quad()
        self._create_shader_program(
            vertex_shader_path,
            fragment_shader_path
        )

    def reload_shaders(self):
        try:
            self._create_shader_program(
                self.vertex_shader_path,
                self.fragment_shader_path
            )

            print("Shaders reloaded successfully.")

        except RuntimeError as error:
            print(error)
            print("Keeping previous shader.")

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

        program = self._compile_program(
            vertex_source,
            fragment_source,
            vertex_shader_path,
            fragment_shader_path,
        )

        vao = self.ctx.vertex_array(
            program,
            [
                (self.vbo, "2f", "in_position"),
            ],
        )


        self.program = program
        self.vao = vao

    def _compile_program(
        self,
        vertex_source,
        fragment_source,
        vertex_shader_path,
        fragment_shader_path,
    ):
        try:
            return self.ctx.program(
                vertex_shader=vertex_source,
                fragment_shader=fragment_source,
            )

        except moderngl.Error as error:
            vertex_numbered = self._number_lines(vertex_source)
            fragment_numbered = self._number_lines(fragment_source)

            raise RuntimeError(
                "Shader compilation/linking failed.\n\n"
                f"Vertex shader: {vertex_shader_path}\n"
                f"{vertex_numbered}\n\n"
                f"Fragment shader: {fragment_shader_path}\n"
                f"{fragment_numbered}\n\n"
                f"Compiler error:\n{error}"
            ) from error
        
    def _number_lines(self, source):
        return "\n".join(
            f"{i:4}: {line}"
            for i, line in enumerate(source.splitlines(), start=1)
        )

    def render(self, time, delta_time, frame):
        self.program["u_time"] = time
        self.program["u_resolution"] = (self.width, self.height)

        self.vao.render()