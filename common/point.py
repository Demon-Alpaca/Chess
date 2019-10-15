class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.pixel_x = 20 + 40 * self.x
        self.pixel_y = 20 + 40 * self.y
