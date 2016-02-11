class Game:
    def __init__(self, orders, warehouses, drones):
        self.orders = orders
        self.warehouses = warehouses
        self.drones = drones

    def order_elems(self, ref, elem_type='warehouses'):
        elems = getattr(self, elem_type)
        sort(elems, key=lambda t: distance(ref.position, t.position))

    def order_

class Order:
    def __init__(self, position=(x, y), products=products, game):
        self.position = position
        self.products = products
        self.game = game

    def deliver(self, product_id, n_product):
        self.products[product_id] -= n_product

    def get_warehouses(self):

class Warehouse:

class Drone: