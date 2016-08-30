from math import ceil

from utils import distance

class Game:
    def __init__(self, orders, warehouses, drones):
        self.orders = orders
        self.warehouses = warehouses
        self.drones = drones
        self.cost_matrix = np.zeros((len(orders), len(drones)))

    def fill_matrix(self):
        for i, order in enumerate(self.orders):
            warehouses, cost = order.evaluate(game)
            self.cost_matrix[i] = cost
            for j, drone in enumerate(self.drones):
                self.cost_matrix[i, j] += drone.evaluate(warehouses)

    def order_warehouses(self, ref):
        distances = list(map(lambda t: distance(ref, t.position), self.warehouses))
        arg_distances = sorted(range(len(distances)), key=lambda t: distances[t])
        return [self.warehouses[i] for i in arg_distances], [distances[i] for i in arg_distances]

    def turn(self):
        for j, drone in enumerate(self.drones):
            if drone.wait == 0:
                drone.affect(self.orders[np.argmin(self.cost_matrix[:, j])])
            else:
                drone.wait -= 1

class Order:
    def __init__(self, order_id, position,
                 products):
        self.id = order_id
        self.position = position
        self.products = products
        self.score_ = 0

    def deliver(self, product_id, n_products):
        self.products[product_id] -= n_products
        if self.products[product_id] < 0:
            self.products[product_id] = 0
            n_products += self.products[product_id]
        return n_products

    def evaluate(self, game):
        self.warehouses_ = []
        products = self.products.copy()
        for warehouse, distance in zip(*game.order_warehouses(self.position)):
            products -= warehouse.products
            self.warehouses_.append(warehouse)
            self.score_ += distance
            if np.all(self.products) < 0:
                break
        return self.warehouses_, self.score_


class Warehouse:
    def __init__(self, warehouse_id, position, products):
        self.id = warehouse_id
        self.position = position
        self.products = products

    def loads(self, product_id, n_products):
        self.products[product_id] -= n_products
        if self.products[product_id] < 0:
            n_products += self.products[product_id]
            self.products[product_id] = 0
        return n_products


class Drone:
    def __init__(self, drone_id, position):
        self.id = drone_id
        self.position = position
        self.products = np.zeros(n_product_types)
        self.wait = 0
        self.weight = 0

    def delivers(self, order, product_id):
        if order.products[product_id] == 0:
            return 1
        else:
            n_products = order.deliver(product_id, self.products[product_id])
            self.products[product_id] -= n_products
            self.weight -= n_products * product_weights[product_id]
            self.wait += 1
            instructions.append([self.id, 'D', order.id, product_id, int(n_products)])
            return 1

    def evaluate(self, warehouses):
        return sum(map(lambda t: distance(t.position, self.position), warehouses))

    def flies(self, position):
        self.wait += int(ceil(distance(position, self.position)))
        self.position = position

    def loads(self, warehouse, product_id, n_product):
        if warehouse.products[product_id] == 0:
            return 1
        self.wait += 1
        n_products = warehouse.loads(product_id, n_product)

        self.weight += n_products * product_weights[product_id]

        if self.weight > max_payload:
            old_n_products = n_products
            n_products -= (max_payload - self.weight) // product_weights[product_id] + 1
            self.weight += (old_n_products - n_products) * product_weights[product_id]
            self.products += n_products
            instructions.append([self.id, 'L', warehouse.id,
                                 product_id, int(n_products)])
            return 0
        else:
            instructions.append([self.id, 'L', warehouse.id,
                                 product_id, int(n_products)])
            return 1

    def affect(self, order):
        for warehouse in order.warehouses_:
            self.flies(warehouse.position)
            for product_id in np.where(order.products)[0]:
                has_space = self.loads(warehouse, product_id,
                                  order.products[product_id])
                if not has_space:
                    break
            self.flies(order.position)
            for product_id in np.where(order.products)[0]:
                self.delivers(order, product_id)

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
        orders.append(((x, y), np.bincount(products, minlength=n_product_types)))

instructions = []
orders_list = []
drones_list = []
warehouses_list = []
for i, order in enumerate(orders):
    orders_list.append(Order(i, order[0], order[1]))
for i, warehouse in enumerate(warehouses):
    warehouses_list.append(Warehouse(i, warehouse[0], warehouse[1]))
for i in range(n_drones):
    drones_list.append(Drone(i, (0, 0)))

game = Game(orders_list, warehouses_list, drones_list)

game.fill_matrix()

for i in range(n_turns):
    print(i)
    game.turn()
for instruction in instructions:
    print(instruction)