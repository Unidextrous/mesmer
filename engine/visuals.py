from pathlib import Path
import tomllib

import moderngl

from .shader_loader import load_shader
from .uniforms import UniformManager
from .parameters import ParameterManager
from .palette import PaletteManager

class VisualManager:
    def __init__(self, renderer, visual_directory, default_vertex_shader):
        self.renderer = renderer
        self.visual_path = Path(visual_directory)
        self.default_vertex_shader = default_vertex_shader

        self.visuals = {}

        self.discover()

    def discover(self):
        for folder in self.visual_path.iterdir():
            if folder.is_dir():
                self.visuals[folder.name] = Visual(
                    folder,
                    self.default_vertex_shader
                )

    def load(self, name):
        visual = self.visuals[name]

        self.renderer.load_visual(visual)

    def load_next(self, name, preset_path=None):
        visual = self.visuals[name]

        self.renderer.load_next_visual(
            visual,
            preset_path
        )

class Visual:
    def __init__(self, path, default_vertex_shader):
        self.path = Path(path)
        self.default_vertex_shader = Path(default_vertex_shader)

        self.metadata = self._load_metadata()

        self.name = self.metadata["name"]

        self.vertex_shader = self._get_vertex_shader()

        self.fragment_shader = (
            self.path / self.metadata["fragment_shader"]
        )

        self.parameter_file = (
            self.path / self.metadata["parameters"]
        )

        self.default_preset = (
            self.path / "presets" / "default.toml"
        )

    def _load_metadata(self):
        metadata_path = self.path / "metadata.toml"

        with metadata_path.open("rb") as file:
            return tomllib.load(file)


    def _get_vertex_shader(self):
        if "vertex_shader" in self.metadata:
            return self.path / self.metadata["vertex_shader"]

        return self.default_vertex_shader


class VisualInstance:
    def __init__(self, ctx, vbo, visual, preset_path=None):
        self.ctx = ctx
        self.vbo = vbo
        self.visual = visual

        self.vertex_shader_path = visual.vertex_shader
        self.fragment_shader_path = visual.fragment_shader

        self.parameter_manager = ParameterManager(
            visual.parameter_file
        )

        if preset_path is None:
            preset_path = visual.default_preset

        self.parameter_manager.load_preset(
            preset_path,
            duration=0.0
        )

        self.parameter_manager.update(0.0)
        
        self.palette_manager = PaletteManager(
            self.parameter_manager.palettes
        )


        self._create_shader_program()

        self._shader_mtimes = {
            self.vertex_shader_path:
                Path(self.vertex_shader_path).stat().st_mtime,

            self.fragment_shader_path:
                Path(self.fragment_shader_path).stat().st_mtime,
        }

    def update(self, delta_time):
        self.parameter_manager.check_reload()
        self.parameter_manager.update(delta_time)

    def render(self, values):
        self.uniforms.update(values)

        self.uniforms.set_palette(
            self.palette_manager.colors
        )

        self.vao.render()

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

    def reload_shaders(self):
        try:
            self._create_shader_program()

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

    def _create_shader_program(self):
        vertex_source = load_shader(
            self.vertex_shader_path
        )

        fragment_source = load_shader(
            self.fragment_shader_path
        )

        try:
            program = self.ctx.program(
                vertex_shader=vertex_source,
                fragment_shader=fragment_source,
            )

        except moderngl.Error as error:
            vertex_numbered = self._number_lines(vertex_source)
            fragment_numbered = self._number_lines(fragment_source)

            raise RuntimeError(
                "Shader compilation/linking failed.\n\n"
                f"Vertex shader: {self.vertex_shader_path}\n"
                f"{vertex_numbered}\n\n"
                f"Fragment shader: {self.fragment_shader_path}\n"
                f"{fragment_numbered}\n\n"
                f"Compiler error:\n{error}"
            ) from error

        self.program = program

        self.uniforms = UniformManager(
            self.program
        )

        self.vao = self.ctx.vertex_array(
            self.program,
            [
                (self.vbo, "2f", "in_position"),
            ],
        )

    def _number_lines(self, source):
        return "\n".join(
            f"{i:4}: {line}"
            for i, line in enumerate(
                source.splitlines(),
                start=1
            )
        )