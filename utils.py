from math import sqrt, ceil


def distance(x, y):
    return ceil(sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2))