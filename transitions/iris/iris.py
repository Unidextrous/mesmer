class Iris:
    def __init__(
        self,
        offset=(0.0, 0.0),
        max_radius=1.0,
        edge_softness=0.0,
        color=(0.0, 0.0, 0.0),
        opacity=1.0,
        duration=6.25,
    ):
        self.offset = offset
        self.max_radius = max_radius
        self.edge_softness = edge_softness
        self.color = color
        self.opacity = opacity
        self.duration = duration

        self.progress = 0.0
        self.direction = 0
        self.active = False

    def start(self, direction=0):
        self.direction = direction
        self.progress = 0.0
        self.active = True

    def update(self, delta_time):
        if not self.active:
            return

        self.progress += delta_time / self.duration

        if self.progress >= 1.0:
            self.progress = 1.0
            self.active = False

    def get_uniforms(self):
        return {
            "u_transition_progress": self.progress,
            "u_iris_offset": self.offset,
            "u_iris_max_radius": self.max_radius,
            "u_iris_edge_softness": self.edge_softness,
            "u_iris_color": self.color,
            "u_iris_opacity": self.opacity,
            "u_iris_direction": self.direction,
            "u_iris_active": 1 if self.active else 0,
        }