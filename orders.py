from utils import distance


class Game:
    def __init__(self, orders, warehouses, drones):
        self.orders = orders
        self.warehouses = warehouses
        self.drones = drones

    def order_elems(self, ref, elem_type):
        elems = getattr(self, elem_type)
        return sorted(elems, key=lambda t: distance(ref.position, t.position))


class Order:
    def __init__(self, position,
                 products, game):
        self.position = position
        self.products = products
        self.game = game

    def deliver(self, product_id, n_product):
        self.products[product_id] -= n_product

    def get_warehouses(self):
        warehouses = []
        for warehouse in self.game.order_elems(self.position, 'warehouses'):


    def cost(self):


class Warehouse:
    def __init__(self, position, products, game):
        self.position = position
        self.products = products

class Drone:
    def __init__(self, position, products, game):
        self.position = position
        self.products = products

    def deliver(self):
        self.products[product_id] -= n_product

    def load(self):