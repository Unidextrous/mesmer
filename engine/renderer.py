from pathlib import Path

import moderngl
import numpy as np

from .shader_loader import load_shader
from .uniforms import UniformManager
from .parameters import ParameterManager
from .palette import PaletteManager

class Renderer:
    def __init__(self, width, height):
        self.ctx = moderngl.create_context()

        self.width = width
        self.height = height

        self._create_quad()
        self._create_framebuffer()

    def _shaders_changed(self):
        for path in (
            self.vertex_shader_path,
            self.fragment_shader_path,
        ):
            current_mtime = Path(path).stat().st_mtime

            if current_mtime != self._shader_mtimes[path]:
                return True

        return False

    def check_shader_reload(self):
        if self._shaders_changed():
            self.reload_shaders()

    def load_visual(self, visual):
        self.vertex_shader_path = visual.vertex_shader
        self.fragment_shader_path = visual.fragment_shader

        self.parameter_manager = ParameterManager(visual.parameter_file)

        self.palette_manager = PaletteManager(
            self.parameter_manager.palettes
        )

        self._create_shader_program(
            self.vertex_shader_path,
            self.fragment_shader_path
        )

        self._shader_mtimes = {
            self.vertex_shader_path:
                Path(self.vertex_shader_path).stat().st_mtime,

            self.fragment_shader_path:
                Path(self.fragment_shader_path).stat().st_mtime,
        }

        print(f"Loaded visual: {visual.name}")

    def reload_shaders(self):
        try:
            self._create_shader_program(
                self.vertex_shader_path,
                self.fragment_shader_path
            )

            self._shader_mtimes = {
                self.vertex_shader_path:
                    Path(self.vertex_shader_path).stat().st_mtime,

                self.fragment_shader_path:
                    Path(self.fragment_shader_path).stat().st_mtime,
            }

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

    def _create_framebuffer(self):
        self.color_texture = self.ctx.texture(
            (self.width, self.height),
            4,
        )

        self.framebuffer = self.ctx.framebuffer(
            color_attachments=[self.color_texture]
        )

    def _create_shader_program(self, vertex_shader_path, fragment_shader_path):
        vertex_source = load_shader(vertex_shader_path)
        fragment_source = load_shader(fragment_shader_path)

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
        self.uniforms = UniformManager(self.program)
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
        self.parameter_manager.check_reload()

        values = dict(self.parameter_manager.values)

        values.update({
            "u_time": time,
            "u_delta_time": delta_time,
            "u_resolution": (self.width, self.height),
            "u_frame": frame,
        })
        
        self.uniforms.update(values)

        self.uniforms.set_palette(
            self.palette_manager.colors
        )

        self.vao.render()