from math import ceil

from utils import distance
import numpy as np

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
            if self.drone_availability[j] >= 0:
                drone.affect(self.orders[np.argmin(self.cost_matrix[:, j])])


class Order:
    def __init__(self, position,
                 products, game):
        self.position = position
        self.products = products
        self.game = game

    def deliver(self, product_id, n_product):
        self.products[product_id] -= n_product
        if np.all(self.products <= 0):
            return True
        else:
            return False

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
    def __init__(self, position, products, game):
        self.position = position
        self.products = products

    def load(self, warehouse, product_id):
        self.products[product] -= n_product

class Drone:
    def __init__(self, drone_id, position, products, game):
        self.position = position
        self.products = products
        self.wait = 0

    def delivers(self, product_id, n_product):
        self.game.instruction.append
        self.products[product_id] -= n_product
        self.wait += 1

    def evaluate(self, warehouses):
        return sum(map(warehouses, lambda t: distance(t.position, self.position)))

    def flies(self, position):
        self.game.instruction.append('')
        self.wait += int(ceil(distance(position, self.position)))
        self.position = position

    def loads(self, product_id, n_product):
        if self.weight + n_product < MAX_WEIGHT:
            self.products[product_id] += n_product
            self.wait += 1
            return 1
        else:
            return 0

    def affect(self, order):
        for warehouse in order.warehouses_:
            self.flies(warehouse)
            for product_id in np.where(order.products)[0]:
                done = self.loads(warehouse, product_id, order.products[product_id])
                if not done:
                    break
            self.flies(order.position)