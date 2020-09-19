class MappingAdapter:
    def __init__(self, adaptee):
        self.adaptee = adaptee

    def lighten(self, map_matrix):
        self.adaptee.set_dim((len(map_matrix[0]), len(map_matrix)))
        obstacles = []
        lights = []

        for row_index, row in enumerate(map_matrix):
            for cell_index, cell in enumerate(row):
                if cell == -1:
                    obstacles.append((cell_index, row_index))
                elif cell == 1:
                    lights.append((cell_index, row_index))

        self.adaptee.set_lights(lights)
        self.adaptee.set_obstacles(obstacles)

        return self.adaptee.generate_lights()
