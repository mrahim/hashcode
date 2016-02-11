class Game:
    def __init__(self, orders, warehouses, drones):
        self.orders = orders
        self.warhouses = warhouses
        self.drones = drones

    def get_closest(self):



class Order:
    def __init__(self, x, y, products, game):
        self.x = x
        self.y =y
        self.products = products

    def deliver(self, product_id, n_product):
        self.products[product_id] -= n_product

    def get_warehouses(self):

class Warehouse:

class Drone: