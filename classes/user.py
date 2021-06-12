class User:
    name = None
    login = None
    password = None
    orders = []

    def __init__(self, name, login, password):
        self.name = name
        self.login = login
        self.password = password

    def add_order(self, order):
        self.orders.append(order)

    def pay_order(self, order_id):
        for order in self.orders:
            if order.id == order_id:
                order.status = "payed"
                return True
        return False

    def print_all_orders(self, catalog):
        if len(self.orders) == 0:
            print("В данный момент у вас нет доступных заказов")
        else:
            for order in self.orders:
                order.print(catalog)
