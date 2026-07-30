from pathlib import Path
import tomllib


class ParameterManager:
    def __init__(self, parameter_path):
        self.parameter_path = Path(parameter_path)

        self._mtime = None
        self.values = {}

        self.reload()

    def reload(self):
        with self.parameter_path.open("rb") as file:
            new_parameters = tomllib.load(file)

        self.values = new_parameters
        self._mtime = self.parameter_path.stat().st_mtime

    def check_reload(self):
        current = self.parameter_path.stat().st_mtime

        if current != self._mtime:
            try:
                self.reload()
                print("Parameters reloaded.")

            except tomllib.TOMLDecodeError as error:
                print(error)
                print("Keeping previous parameters")