from math import ceil

from utils import distance
import numpy as np

global MAX_WEIGHT
global INSTRUCTION
global WEIGHTS

class Game:
    def __init__(self, orders, warehouses, drones):
        self.orders = orders
        self.warehouses = warehouses
        self.drones = drones
        self.cost_matrix = np.array(len(orders), len(drones))

    def fill_matrix(self):
        for i, order in enumerate(self.orders):
            warehouses, cost = order.evaluate()
            self.cost_matrix[i] = cost
            for j, drone in enumerate(self.drones):
                self.cost_matrix[i, j] += drone.evaluate(warehouses)

    def order_elems(self, ref, elem_type):
        elems = getattr(self, elem_type)
        distances = map(elems, lambda t: distance(ref.position, t.position))
        return sorted(elems, key=distances), sorted(distances)

    def turn(self):
        for j, drone in enumerate(self.drones):
            if drone.wait == 0:
                drone.affect(self.orders[np.argmin(self.cost_matrix[:, j])])
            else:
                drone.wait -= 1
        self.fill_matrix()

class Order:
    def __init__(self, order_id, position,
                 products):
        self.id = order_id
        self.position = position
        self.products = products

    def deliver(self, product_id, n_products):
        self.products[product_id] -= n_products
        if self.products[product_id] < 0:
            self.products[product_id] = 0
            n_products += self.products[product_id]
        return n_products

    def evaluate(self):
        self.warehouses_ = []
        products = self.products.copy()
        for warehouse, distance in self.game.order_elems(self.position, 'warehouses'):
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
    def __init__(self, drone_id, position, products):
        self.id = drone_id
        self.position = position
        self.products = products
        self.wait = 0
        self.weight = 0

    def delivers(self, order, product_id):
        if order.products[product_id] == 0:
            return 1
        else:
            n_products = order.deliver(product_id, self.products[product_id])
            self.products[product_id] -= n_products
            self.weight -= n_products * self.game.weights[product_id]
            self.wait += 1
            INSTRUCTIONS.append([self.id, 'D', order.id, product_id, n_products])
            return 1

    def evaluate(self, warehouses):
        return sum(map(warehouses, lambda t: distance(t.position, self.position)))

    def flies(self, position):
        self.wait += int(ceil(distance(position, self.position)))
        self.position = position

    def loads(self, warehouse, product_id, n_product):
        if warehouse.products[product_id] == 0:
            return 1
        self.wait += 1
        n_products = warehouse.loads(product_id, n_product)

        self.weight += n_products * WEIGHTS[product_id]

        if self.weight > MAX_WEIGHTS:
            old_n_products = n_products
            n_products -= (MAX_WEIGHTS - self.weight) // WEIGHTS[product_id] + 1
            self.weight += (old_n_products - n_products) * WEIGHTS[product_id]
            self.products += n_products
            INSTRUCTIONS.append([self.id, 'L', warehouse.id,
                                 product_id, n_products)
            return 0
        else:
            return 1

    def affect(self, order):
        for warehouse in order.warehouses_:
            self.flies(warehouse)
            for product_id in np.where(order.products)[0]:
                has_space = self.loads(warehouse, product_id,
                                  order.products[product_id])
                if not has_space:
                    break
            self.flies(order.position)
            for product_id in np.where(order.products)[0]:
                self.delivers(order, product_id)


def main():
    global INSTRUCTION = []
    global MAX_WEIGHTS = 100
    global WEIGHTS =
    orders = []
    for i in range(n_orders):
        orders.append(Order(i))
    for i in range(n_warehouses):
    for i i