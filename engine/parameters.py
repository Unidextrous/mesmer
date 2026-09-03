from pathlib import Path
import tomllib


class ParameterManager:
    def __init__(self, parameter_path):
        self.parameter_path = Path(parameter_path)

        self._mtime = None

        self.values = {}
        self.start_values = {}
        self.target_values = {}

        self.palettes = {}

        self.transition_time = 0.0
        self.transition_duration = 1.0

        self.reload()

    def reload(self):
        with self.parameter_path.open("rb") as file:
            new_parameters = tomllib.load(file)

        new_values = {}
        new_palettes = {}

        for name, value in new_parameters.items():

            if name == "u_palette":
                new_palettes[name] = value

            else:
                new_values[name] = value

        if not self.values:
            self.values = new_values.copy()

        else:
            self.start_values = self.values.copy()
            self.transition_time = 0.0

        self.target_values = new_values
        self.palettes = new_palettes

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

    def update(self, delta_time):
        if not self.values:
            return

        if self.transition_time >= self.transition_duration:
            self.values = self.target_values.copy()
            return

        self.transition_time += delta_time

        progress = min(
            self.transition_time /
            self.transition_duration,
            1.0
        )

        for name, target in self.target_values.items():

            start = self.start_values.get(
                name,
                target
            )

            if isinstance(target, list):
                self.values[name] = [
                    start_value +
                    (target_value - start_value) * progress

                    for start_value, target_value
                    in zip(start, target)
                ]

            elif isinstance(target, float):
                self.values[name] = (
                    start +
                    (target - start) * progress
                )

            else:
                self.values[name] = target

    def load_preset(self, preset_path, duration=1.0):
        preset_path = Path(preset_path)

        with preset_path.open("rb") as file:
            new_parameters = tomllib.load(file)

        new_values = {}
        new_palettes = {}

        for name, value in new_parameters.items():

            if name == "u_palette":
                new_palettes[name] = value

            else:
                new_values[name] = value

        self.start_values = self.values.copy()
        self.target_values = new_values
        self.palettes = new_palettes

        self.transition_duration = duration
        self.transition_time = 0.0