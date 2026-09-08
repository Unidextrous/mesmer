from pathlib import Path

import moderngl
import numpy as np
import math

from .uniforms import UniformManager
from .shader_loader import load_shader
from .visuals import VisualInstance

from transitions.iris.iris import Iris

class Renderer:
    def __init__(self, width, height):
        self.ctx = moderngl.create_context()

        self.width = width
        self.height = height

        self.phase = 0.0

        self._create_quad()
        self._create_framebuffers()
        self._create_display_program()

        self.iris = Iris()

    def load_visual(self, visual):
        self.current_visual_instance = VisualInstance(
            self.ctx,
            self.vbo,
            visual,
        )

        print(f"Loaded current visual: {visual.name}")

    def load_next_visual(self, visual, preset_path=None):
        self.next_visual_instance = VisualInstance(
            self.ctx,
            self.vbo,
            visual,
            preset_path
        )

        print(f"Loaded next visual: {visual.name}")

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

    def _create_framebuffers(self):
        self.current_texture = self.ctx.texture(
            (self.width, self.height),
            4,
        )

        self.current_framebuffer = self.ctx.framebuffer(
            color_attachments=[self.current_texture]
        )

        self.next_texture = self.ctx.texture(
            (self.width, self.height),
            4,
        )

        self.next_framebuffer = self.ctx.framebuffer(
            color_attachments=[self.next_texture]
        )

    def _create_display_program(self):
        vertex_source = load_shader(
            "engine/shaders/display.vert"
        )

        fragment_source = load_shader(
            "engine/shaders/display.frag"
        )

        program = self._compile_program(
            vertex_source,
            fragment_source,
            "engine/shaders/display.vert",
            "engine/shaders/display.frag",
        )

        vao = self.ctx.vertex_array(
            program,
            [
                (self.vbo, "2f", "in_position"),
            ],
        )

        self.display_program = program
        self.display_vao = vao
        self.display_uniforms = UniformManager(
            self.display_program
        )

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

    def _complete_transition(self):
        self.current_visual_instance, self.next_visual_instance = (
            self.next_visual_instance,
            self.current_visual_instance,
        )

        self.current_texture, self.next_texture = (
            self.next_texture,
            self.current_texture,
        )

        self.current_framebuffer, self.next_framebuffer = (
            self.next_framebuffer,
            self.current_framebuffer,
        )

        print(
            f"Transition complete. "
            f"Current visual: {self.current_visual_instance.visual.name}"
        )

    def render(self, time, delta_time, frame):
        self.current_visual_instance.check_shader_reload()
        self.next_visual_instance.check_shader_reload()

        self.current_visual_instance.parameter_manager.check_reload()
        self.next_visual_instance.parameter_manager.check_reload()

        self.current_visual_instance.parameter_manager.update(delta_time)
        self.next_visual_instance.parameter_manager.update(delta_time)

        transition_complete = self.iris.update(delta_time)

        phase_speed = self.current_visual_instance.parameter_manager.values.get(
            "u_cycle_speed",
            0.0
        )

        self.phase += phase_speed * delta_time
        self.phase %= 2.0 * math.pi

        global_values = {
            "u_time": time,
            "u_delta_time": delta_time,
            "u_resolution": (self.width, self.height),
            "u_frame": frame,
            "u_phase": self.phase,
        }

        current_values = dict(
            self.current_visual_instance.parameter_manager.values
        )

        current_values.update(global_values)

        next_values = dict(
            self.next_visual_instance.parameter_manager.values
        )

        next_values.update(global_values)
        
        self.display_uniforms.update(global_values)

        self.display_uniforms.update(
            self.iris.get_uniforms()
        )

        self.current_visual_instance.uniforms.set_palette(
            self.current_visual_instance.palette_manager.colors
        )

        self.current_framebuffer.use()
        self.current_visual_instance.render(current_values)

        self.next_framebuffer.use()
        self.next_visual_instance.render(next_values)

        self.ctx.screen.use()

        if transition_complete:
            self._complete_transition()
            
        self.current_texture.use(location=0)
        self.next_texture.use(location=1)

        self.display_program["u_current_texture"] = 0
        self.display_program["u_next_texture"] = 1

        self.display_vao.render()
