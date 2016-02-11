import numpy as np
from math import sqrt, ceil

def distance(x, y):
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def time_turns(d):
    return ceil(d)

def order_weight(orders, product_weights):
    return [np.dot(order[1], product_weights) for order in orders]
