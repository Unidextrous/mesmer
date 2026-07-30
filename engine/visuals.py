from pathlib import Path
import tomllib

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

    def _load_metadata(self):
        metadata_path = self.path / "metadata.toml"

        with metadata_path.open("rb") as file:
            return tomllib.load(file)


    def _get_vertex_shader(self):
        if "vertex_shader" in self.metadata:
            return self.path / self.metadata["vertex_shader"]

        return self.default_vertex_shader