class Order:
    id = None
    date_created = None
    status = None
    positions = []

    def __init__(self, order_id, date_created, status, positions):
        self.id = order_id
        self.date_created = date_created
        self.status = status
        self.positions = positions

    def add_item(self, item_name, count):
        self.positions[item_name] = count

    def edit_item(self, item_name, new_count):
        self.positions[item_name] = new_count

    def remove_item(self, item_name):
        del self.positions[item_name]

    def print(self, catalog):
        total = 0
        print()
        print("Заказ №: ", self.id)
        print("Создан: ", self.date_created)
        print("Статус заказ: ", self.status)
        if len(self.positions) == 0:
            print("Ваш заказ пуст. Перейдите в каталог, чтобы добавить товары в ваш заказ.")
        else:
            print("Ваш заказ состоит из:")
            for position in self.positions:
                item = catalog.get_item(position[0])
                item.print()
                print("У вас в корзине: ", position[1])
                total += item.count * position[1]
                print()
            print("Итого: ", total)
            print()

