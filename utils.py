from math import sqrt, ceil

def distance(x, y):
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def time_turns(d):
    return ceil(d)

