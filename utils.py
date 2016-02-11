from math import sqrt, ceil

def distance(x, y):
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)

def time_turns(d):
    return ceil(d)


def order_weight(orders, product_weights):
    cost = 0
    for order in orders:
        products_type = order[1]
        for p in products_type:
            cost += product_weights[p]
    return cost
