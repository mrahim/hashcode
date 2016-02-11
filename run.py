import numpy as np
import sys


global_line = 0


def read_n_int(f, n):
    global global_line
    line = f.readline().split()
    values = [int(x) for x in line]
    global_line += 1
    if len(values) != n:
        raise ValueError('Expected number of values is not right in line %i' %
                         global_line)
    return values

if len(sys.argv) < 2:
    raise ValueError('Usage run.py <file>')

with open(sys.argv[1]) as f:
    n_rows, n_cols, n_drones, n_turns, max_payload = read_n_int(f, 5)
    n_product_types = read_n_int(f, 1)[0]
    product_weights = read_n_int(f, n_product_types)
    n_warehouses = read_n_int(f, 1)[0]

    # List of (x, y, products)
    warehouses = []
    for i in range(n_warehouses):
        x, y = read_n_int(f, 2)
        products = read_n_int(f, n_product_types)
        warehouses.append(((x, y), products))
    n_orders = read_n_int(f, 1)[0]

    # List of (x, y, products)
    orders = []
    for i in range(n_orders):
        x, y = read_n_int(f, 2)
        n_items = read_n_int(f, 1)[0]
        products = read_n_int(f, n_items)
        orders.append(((x, y), np.bincount(products)))


