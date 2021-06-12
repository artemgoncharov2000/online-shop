from classes.catalog import Catalog
from dbmanager import create_data, get_all_items, get_user_by_login, get_orders_by_login, del_pos_from_order, \
    create_order, get_order_by_id, add_item_to_order, update_order, update_position


class App:
    user = None
    catalog = None
    '''
        Initializes client's app
    '''

    def __init__(self):

        try:
            create_data()
        except Exception:
            print("Данные уже загружены")

        items = get_all_items()
        self.catalog = Catalog(items)

    '''
        Makes auth process 
    '''

    def auth(self):
        while True:
            login = input('Введите ваш логин: ').lower()
            password = input("Введите ваш пароль: ")

            try:
                user = get_user_by_login(login)
                if user.login == login and user.password == password:
                    print("Вы успешно авторизовались!")
                    print(f"Рады вас снова видеть, {user.name}!")
                    self.user = user
                    self.user.orders = get_orders_by_login(self.user.login)
                    break
            except Exception as e:
                print("Неверно введены логин или пароль")
                print("Нажмите enter, чтобы попробовать еще раз")
                print("Введите back, чтобы вернуться назад")

            response = input('Команда: ')
            if response == "back":
                break

    '''
        Prints all items in catalog
    '''

    def show_catalog(self):
        while True:
            print()
            self.catalog.print()
            if self.user is not None:
                print("add {item_name} {count}: Добавить в заказ")
            print("back: Назад")
            response = input()
            if "add" in response and self.user is not None:
                try:
                    response = response.split(" ")
                    item_name = response[1]
                    item_count = int(response[2])
                    if item_count > self.catalog.get_item(item_name).count:
                        raise ValueError("К сожалению, в магазине нет такого количество товара. Пожалуйста, введите "
                                         "другое количество!")
                    self.user.print_all_orders(self.catalog)
                    print("{order_id}: Выберите заказ, в который хотите добавить товар")
                    order_id = input("Номер заказа: ")
                    add_item_to_order(order_id, item_name, item_count)
                    self.user.orders = get_orders_by_login(self.user.login)
                    print('Вы успешно добавили товар в заказ!')
                except ValueError as ve:
                    print(ve)
                except Exception as e:
                    print('Не удалось добавить товар в заказ. Попробуйте еще раз!')

            elif response == "back":
                break
            else:
                print("К сожалению, такой команды нет:(")

    '''
        Prints list of user's orders
    '''

    def show_orders(self):
        while True:
            self.user.print_all_orders(self.catalog)
            print()
            print("open {order_id}: Открыть заказ №")
            print("create: Создать эаказ")
            print("back: Назад")
            response = input("Команда: ")
            if "open" in response:
                try:
                    response = response.split(" ")
                    order_id = response[1]
                    self.show_order(order_id)
                except Exception:
                    print('Неверный номер заказа. Попробуйте еще раз!')
            elif response == "create":
                try:
                    create_order(self.user.login)
                    self.user.orders = get_orders_by_login(self.user.login)
                    print("Заказ был успешно создан!")
                except Exception as e:
                    print(e)
                    print("Не удалось создать заказ. Повторите попытку!")
            elif response == "back":
                break
            else:
                print("К сожалению, такой команды нет:(")

    def check_items(self, order):
        for pos in order.positions:
            for item in self.catalog.items:
                if item.name is pos[0] and item.count < pos[1]:
                    return False
        return True

    ''' 
        Prints order's info
    '''

    def show_order(self, order_id):
        while True:
            order = get_order_by_id(order_id)
            order.print(self.catalog)
            print()
            if len(order.positions) != 0 and order.status != 'Оплачен':
                print("edit {name} {count}: Изменить количество товара")
                print("del {item_name}: Удалить товар из заказа")
            if order.status != 'Оплачен':
                print("pay: Оплатить заказ")
            print("back: Вернуться назад")
            response = input("Команда: ")
            if 'edit' in response and len(order.positions) != 0 and order.status != 'Оплачен':
                try:
                    response = response.split(" ")
                    item_name = response[1]
                    new_count = int(response[2])
                    if new_count > self.catalog.get_item(item_name).count:
                        raise ValueError("К сожалению, в магазине нет такого количество товара. Пожалуйста, введите "
                                         "другое количество!")
                    if new_count <= 0:
                        raise ValueError("Количество товара не может быть меньше нуля.")
                    update_position(order.id, item_name, new_count)
                    self.user.orders = get_orders_by_login(self.user.login)
                except ValueError as ve:
                    print(ve)
                except Exception:
                    print("Не удалось изменить количество добавленного товара. Попробуйте еще раз!")
            elif 'del' in response and len(order.positions) != 0 and order.status != 'Оплачен':
                try:
                    response = response.split(" ")
                    item_name = response[1]
                    del_pos_from_order(order.id, item_name)
                    self.user.orders = get_orders_by_login(self.user.login)
                except Exception:
                    print('Не удалось удалить позицию из заказа, попробуйте еще раз!')
            elif response == 'pay' and order.status != 'Оплачен':
                try:
                    if not self.check_items(order):
                        raise Exception('Недостаточно товаров на складе. Уменьшите количество товаром!')
                    update_order(order.id, 'Оплачен')
                    print("Заказ успешно оплачен!")
                except Exception as e:
                    print(e)
            elif response == "back":
                break

    '''
        Starts the app
    '''

    def start(self):
        print("Здравствуйте, добро пожаловать в наш Интернет-магазин!")
        while True:
            print("Пожалуйста, выберите одну из следующих команд:")
            if self.user is None:
                print("auth: Авторизоваться")
            else:
                print("signout: Выйти из аккаунта")
            print("catalog: Посмотреть каталог товаров")
            if self.user is not None:
                print("orders: Посмотреть мои заказы")
            print("exit: Завершить работу программы")

            response = input("Команда: ")
            if response == "auth" and self.user is None:
                self.auth()
            elif response == "signout" and self.user is not None:
                self.user = None
            elif response == "catalog":
                self.show_catalog()
            elif response == "orders" and self.user is not None:
                self.show_orders()
            elif response == "exit":
                print("Спасибо, что пользуйтесь нашим интернет магазином!")
                print("До скорой встречи!")
                break
            else:
                print("К сожалению, такой команды нет:(")


app = App()
app.start()
