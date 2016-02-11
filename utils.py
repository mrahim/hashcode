from math import sqrt

def distance(x, y):
    return sqrt((x[0] - y[0]) ** 2 + (x[1] - y[1]) ** 2)
    
    
def order_weight(products_in_order, product_weights):
    cost = 0    
    for product, weight in zip(order, product_weights):
        cost += product*weight
    return cost
