import numpy as np

class UniformManager:
    def __init__(self, program):
        self.program = program

        self.available_uniforms = {
            name
            for name in program
            if not name.startswith("in_")
        }

    def update(self, values):
        for name, value in values.items():
            if name in self.available_uniforms:
                self.program[name] = value

    def set_palette(self, palette):

        if "u_palette" not in self.program:
            return

        padded = list(palette)

        while len(padded) < 8:
            padded.append(palette[-1])

        data = np.array(
            padded,
            dtype="f4"
        )

        self.program["u_palette"].write(
            data.tobytes()
        )