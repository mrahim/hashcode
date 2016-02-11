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
        warehouses.append((x, y, products))

    pos_whs = np.asarray([[n[0], n[1]] for n in warehouses])
    cnt_whs = np.asarray([n[2] for n in warehouses])

    n_orders = read_n_int(f, 1)[0]

    # List of (x, y, products)
    orders = []
    for i in range(n_orders):
        x, y = read_n_int(f, 2)
        n_items = read_n_int(f, 1)[0]
        products = read_n_int(f, n_items)
        orders.append((x, y, np.bincount(products)))

    pos_ord = np.asarray([[n[0], n[1]] for n in orders])
    cnt_ord = np.asarray([n[2] for n in orders])


pos_drn = np.repeat([pos_whs[0]], n_drones, axis=0)
cnt_drn = np.zeros((n_drones, n_product_types))


def dist(c1, c2):
    return np.sqrt((c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2)


def get_products_from_warehouse(o_id, w_id, type, n_prod):
    cost = dist(pos_ord[o_id], pos_whs[w_id]) * 2
    trips = max_payload / (product_weights[type] * n_prod)
    return trips * cost




def get_cost_order(o_id):
    prods = cnt_ord[o_id]
    cost = 0
    c_whs, whs = get_dist_warehouses(o_id)
    for p_id, p_cnt in zip(range(n_prod), prods):
        for i_whs in whs:
            get_products_from_warehouse(o_id, w_id, p_id, p_cnt)
    return cost


def get_best_order():
    # Crawl the orders
    # Estimate cost
    # Resolve cheapest order

    for order in orders:
        pass


def get_closest_wh_with(o_id, p_id):
    costs = []
    ids = []
    for w_id in range(n_warehouses):
        if cnt_whs[p_id] > 1:
            ids.append(w_id)
            costs.append(dist(pos_ord[o_id], pos_whs[w_id]))
    argmin = np.argmin(costs)
    return ids[argmin], costs[argmin]


def get_closest_drn(o_id):
    dists = []
    for d_id in range(n_drones):
        dists.append(dist(pos_ord[o_id], pos_drn[d_id]))
    return np.argmin(dists)


def generate_atomic_insts():

    insts = []

    # Generate atomic instructions

    for o_id in range(n_orders):
        for p_id in range(n_product_types):
            if cnt_ord[p_id] == 0:
                continue
            w_id, cst = get_closest_wh_with(o_id, p_id)
            insts.append((o_id, w_id, p_id, cnt_ord[p_id] * cst))

    # Estimate cost per order

    order = np.zeros((n_orders,))
    for inst in insts:
        order[inst[0]] += inst[3]

    # Reorder instructions according to estimated cost
    new_insts = []
    for i in np.argsort(order):
        for inst in insts:
            if inst[0] == i:
                new_insts.append(inst)

    insts = new_insts

    # Now, in two times:
    # - on inst find the closest drone to be fulfilled
    # - the drone takes other insts to fulfill

    timer = 0
    drones = np.zeros(n_drones)

    while(True):
        inst, insts = insts[0], insts[1:]
        o_id, w_id, p_id, _ = inst
        d_id = get_closest_drn(o_id)

        cnt_whs[w_id][p_id] = cnt_whs[w_id][p_id] - 1 

        d_insts = [inst]
        # Now look for other actions doable
        for inst in insts:
            if inst[0] == o_id and inst[1] == w_id:

            
