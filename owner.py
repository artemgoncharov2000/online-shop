from classes.catalog import Catalog
from classes.item import Item
from classes.user import User
from dbmanager import create_data, get_all_items, get_user_by_login, get_orders_by_login, update_item, get_open_orders, \
    update_order


class App:
    catalog = None

    '''
        Initializes owner's app
    '''
    def __init__(self):
        try:
            create_data()
        except Exception:
            print("Данные уже загружены")
        items = get_all_items()
        self.catalog = Catalog(items)

    '''
        Updates item's price 
         
    '''
    def edit_item_price(self, item_name, new_price):
        try:
            if new_price < 0:
                raise ValueError("Цена товара не может быть меньше нуля.")
            item = self.catalog.get_item(item_name)
            item.price = new_price
            update_item(item)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print("Не удалось обновить цену товара. Попробуйте еще раз!")

    '''
        Updates item's count
    '''
    def edit_item_count(self, item_name, new_count):
        try:
            if new_count <= 0:
                raise ValueError("Количество товара не может быть меньше нуля.")
            item = self.catalog.get_item(item_name)
            item.count = new_count
            update_item(item)
        except ValueError as ve:
            print(ve)
        except Exception as e:
            print("Не удалось обновить цену товара. Попробуйте еще раз!")

    '''
        Prints all items in catalog
    '''
    def show_catalog(self):
        while True:
            self.catalog.print()
            print("edit price {name} {new price}: Изменить цену товару")
            print("edit count {name} {new count}: Изменить количество товара")
            print("back: Назад")
            response = input('Команда: ')
            if 'edit' in response and 'price' in response:
                try:
                    response = response.split(" ")
                    item_name = response[2]
                    new_item_price = int(response[3])
                    self.edit_item_price(item_name, new_item_price)
                except Exception:
                    print('Неверная команда или данные. Попробуйте еще раз!')
            elif 'edit' in response and 'count' in response:
                try:
                    response = response.split(" ")
                    item_name = response[2]
                    new_item_count = int(response[3])
                    self.edit_item_count(item_name, new_item_count)
                except Exception:
                    print('Неверная команда или данные. Попробуйте еще раз!')
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
            if len(orders) is 0:
                print("В данный момент нет открытых заказов!")
                break
            else:
                for order in orders:
                    order.print(self.catalog)
            print("set {order_id} {Отправлен or Доставлен}: Сделать статус заказа Отправлен/Доставлен")
            print("back: Назад")
            response = input('Команда: ')
            if 'set' in response:
                try:
                    response = response.split(" ")
                    order_id = response[1]
                    status = response[2]
                    update_order(order_id, status)
                except Exception:
                    print("Неверная команда или данные. Попробуйте еще раз!")
            elif response == "back":
                break
            else:
                print("К сожалению, такой команды нет:(")

    '''
        Starts the app
    '''
    def start(self):
        while True:
            print("catalog: Посмотреть каталог товаров")
            print("orders: Посмотреть открытые заказы")
            print("exit: Завершить работу программы")

            response = input('Команда: ')
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
