from pathlib import Path
import tomllib


class ParameterManager:
    def __init__(self, parameter_path):
        self.parameter_path = Path(parameter_path)

        self._mtime = None

        self.values = {}
        self.palettes = {}

        self.reload()

    def reload(self):
        with self.parameter_path.open("rb") as file:
            new_parameters = tomllib.load(file)

        self.values = {}
        self.palettes = {}
        for name, value in new_parameters.items():

            if name == "u_palette":
                self.palettes[name] = value

            else:
                self.values[name] = value

        self._mtime = self.parameter_path.stat().st_mtime

    def check_reload(self):
        current = self.parameter_path.stat().st_mtime

        if current != self._mtime:
            try:
                self.reload()
                print("Parameters reloaded.")

            except tomllib.TOMLDecodeError as error:
                print(error)
                print("Keeping previous parameter values.")