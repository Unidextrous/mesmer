class PaletteManager:
    def __init__(self, palettes):
        self.colors = palettes.get(
            "u_palette",
            []
        )

    @property
    def size(self):
        return len(self.colors)