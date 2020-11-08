import numpy as m


def f1(i, j):
    return " "


class Map:
    def __init__(self, w, h, holes):
        self.map = m.fromfunction(f1, (h, w))
        self.number_holes = holes

    def wallsFloor(self, number_holes):
        return


if __name__ == "__main__":
    m = Map(15, 7, 3)
    print(m.map)
