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