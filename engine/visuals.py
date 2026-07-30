class VisualManager:
    def __init__(self, renderer):
        self.renderer = renderer

        self.visuals = {
            "gradient": {
                "vertex": "visuals/vertex.vert",
                "fragment": "visuals/gradient/shader.frag",
                "parameters": "visuals/gradient/parameters.toml",
            },

            "spiral": {
                "vertex": "visuals/vertex.vert",
                "fragment": "visuals/spiral/shader.frag",
                "parameters": "visuals/spiral/parameters.toml",
            },
        }

        self.current = None

    def load(self, name):
        visual = self.visuals[name]

        self.renderer.load_visual(
            visual["vertex"],
            visual["fragment"],
            visual["parameters"],
        )

        self.current = name

        print(f"Loaded visual: {name}")