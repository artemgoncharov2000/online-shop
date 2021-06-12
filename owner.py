from classes.catalog import Catalog
from classes.item import Item
from classes.user import User
from dbmanager import create_data, get_all_items, get_user_by_login, get_orders_by_login, update_item, get_open_orders, \
    update_order


class App:
    catalog = None

    def __init__(self):
        try:
            create_data()
        except Exception:
            print("Данные уже загружены")
        items = get_all_items()
        self.catalog = Catalog(items)

    def edit_item_price(self, item_name, new_price):
        item = self.catalog.get_item(item_name)
        item.price = new_price
        update_item(item)

    def edit_item_count(self, item_name, new_count):
        item = self.catalog.get_item(item_name)
        item.count = new_count
        update_item(item)

    '''
        Prints all items in catalog
    '''
    def show_catalog(self):
        while True:
            self.catalog.print()
            print("edit price {name} {new price}: Изменить цену товару")
            print("edit count {name} {new count}: Изменить количество товара")
            print("back: Назад")
            response = input("Ваша команда: ")
            if 'edit' in response and 'price' in response:
                response = response.split(" ")
                item_name = response[2]
                new_item_price = int(response[3])
                self.edit_item_price(item_name, new_item_price)
            elif 'edit' in response and 'count' in response:
                response = response.split(" ")
                item_name = response[2]
                new_item_count = int(response[3])
                self.edit_item_count(item_name, new_item_count)
            elif response == "back":
                break
            else:
                print("К сожалению, такой команды нет:(")
    '''
        Prints list of user's orders
    '''
    def show_orders(self):
        while True:
            orders = get_open_orders()
            for order in orders:
                order.print(self.catalog)
            print("set {order_id} {Отправлен or Доставлен}: Сделать статус заказа Отправлен/Доставлен")
            print("back: Назад")
            response = input()
            if 'set' in response:
                response = response.split(" ")
                order_id = response[1]
                status = response[2]
                update_order(order_id, status)
            elif response == "back":
                break
            else:
                print("К сожалению, такой команды нет:(")
    # '''
    #     Prints order's info
    # '''
    # def show_order(self, order_id):
    #     order = None
    #     for o in self.user.orders:
    #         if o.id == order_id:
    #             order = o
    #             break
    #     while True:
    #         order.print()
    #         print("add: Добавить товары из каталога")
    #         print("edit {name} {count}: Изменить количество товара")
    #         print("del {name}: Удалить товар из заказа")
    #         print("pay: Оплатить заказ")
    #         print("back: Вернуться назад")
    #         response = input("Команда: ")
    #         if response == 'add':
    #             self.show_catalog()
    #         elif 'edit' in response:
    #             print()
    #         elif 'del' in response:
    #             print()
    #         elif response == 'pay':
    #             # TODO: Check if all items are on stock
    #             order.status = 'Оплачен'
    #         elif response == "back":
    #             break
    '''
        Starts the app
    '''
    def start(self):
        while True:
            print("catalog: Посмотреть каталог товаров")
            print("orders: Посмотреть открытые заказы")
            print("exit: Завершить работу программы")

            response = input()
            if response == "catalog":
                self.show_catalog()
            elif response == "orders":
                self.show_orders()
            elif response == "exit":
                print("Спасибо, что пользуйтесь нашим интернет магазином!")
                print("До скорой встречи!")
                break
            else:
                print("К сожалению, такой команды нет:(")


app = App()
app.start()
