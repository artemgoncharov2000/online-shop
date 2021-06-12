import sqlite3
from datetime import datetime
import random

from classes.item import Item
from classes.order import Order
from classes.user import User


def create_data():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    Login text NOT NULL PRIMARY KEY,
                    Name text,
                    Password text NOT NULL
                )
            """)

    sql.execute("INSERT INTO users VALUES ('artem2000', 'Артем','password')")
    sql.execute("INSERT INTO users VALUES ('andrew17', 'Андрей','password')")
    sql.execute("INSERT INTO users VALUES ('ser1977', 'Сергей','password')")

    sql.execute("""
                    CREATE TABLE IF NOT EXISTS items (
                        ItemId text NOT NULL PRIMARY KEY,
                        Price int,
                        Count int 
                    )
            """)

    sql.execute("INSERT INTO items VALUES ('Яблоко', 15, 10)")
    sql.execute("INSERT INTO items VALUES ('Груша', 10, 15)")
    sql.execute("INSERT INTO items VALUES ('Апельсин',  20, 20)")

    sql.execute("""
                    CREATE TABLE IF NOT EXISTS orders (
                        OrderId text NOT NULL PRIMARY KEY,
                        DateCreated text,
                        Status text,
                        UserLogin text REFERENCES users(Login)
                    )
            """)
    sql.execute("INSERT INTO orders VALUES ('1', '20/07/2020', 'Создан', 'artem2000')")
    sql.execute("INSERT INTO orders VALUES ('2', '20/07/2020', 'Оплачен', 'artem2000')")
    sql.execute("INSERT INTO orders VALUES ('3', '20/07/2020', 'Оплачен', 'artem2000')")

    sql.execute("""
                    CREATE TABLE IF NOT EXISTS order_items (
                        OrderId text NOT NULL,
                        ItemId text NOT NULL,
                        Count int NOT NULL,
                        FOREIGN KEY (OrderId) REFERENCES orders(OrderId),
                        FOREIGN KEY (ItemId) REFERENCES items(ItemId),
                        UNIQUE (OrderId, ItemId)
                    )
            """)

    sql.execute("INSERT INTO order_items VALUES ('1', 'Яблоко', 5)")
    sql.execute("INSERT INTO order_items VALUES ('2', 'Груша', 7)")
    sql.execute("INSERT INTO order_items VALUES ('3', 'Апельсин', 8)")

    db.commit()


def get_all_items():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    items = []
    for item in sql.execute("SELECT * FROM items"):
        items.append(Item(item[0], item[1], item[2]))

    return items


def get_user_by_login(login):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    user = None
    sql.execute(f"SELECT * FROM users Where Login='{login}'")
    for row in sql.fetchall():
        user = User(row[1], row[0], row[2])
    return user


def get_orders_by_login(login):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    orders = []
    sql.execute(f"SELECT * FROM orders WHERE UserLogin='{login}'")
    for row in sql.fetchall():
        positions = get_position_by_order(row[0])
        orders.append(Order(row[0], row[1], row[2], positions))
    return orders


def check_unique(order_id):
    orders = get_all_orders()
    for order in orders:
        if order.id == order_id:
            return False
    return True


def create_order(login):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    date_created = str(datetime.now())
    order_id = str(random.randint(100000, 999999))
    while not check_unique(order_id):
        order_id = str(random.randint(100000, 999999))
    sql.execute(f"INSERT INTO orders VALUES ('{order_id}', '{date_created}', 'Создан', '{login}')")
    db.commit()


def get_position_by_order(order_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    positions = []
    sql.execute(f"SELECT * FROM order_items WHERE OrderId='{order_id}'")
    for row in sql.fetchall():
        positions.append([row[1], row[2]])
    return positions


def del_pos_from_order(order_id, item_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"DELETE FROM order_items WHERE OrderId='{order_id}' AND ItemId='{item_id}'")
    db.commit()


def update_item(item):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE items SET Price={item.price}, Count={item.count} WHERE ItemId='{item.name}'")
    db.commit()


def get_item_by_id(item_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"SELECT * FROM items WHERE ItemId='{item_id}'")
    item = sql.fetchall()
    return Item(item[0], item[1], item[2])


def get_all_orders():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute("SELECT * FROM orders")
    orders = []
    for row in sql.fetchall():
        positions = get_position_by_order(row[0])
        orders.append(Order(row[0], row[1], row[2], positions))
    return orders


def get_order_by_id(order_id):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    order = None
    for row in sql.execute(f"SELECT * FROM orders WHERE OrderId='{order_id}'"):
        positions = get_position_by_order(row[0])
        order = Order(row[0], row[1], row[2], positions)
    return order


def get_open_orders():
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute("SELECT * FROM orders WHERE Status='Оплачен'")
    orders = []
    for row in sql.fetchall():
        positions = get_position_by_order(row[0])
        orders.append(Order(row[0], row[1], row[2], positions))
    return orders


def add_item_to_order(order_id, item_name, item_count):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"INSERT INTO order_items VALUES ('{order_id}', '{item_name}', {item_count})")
    db.commit()


def update_order(order_id, status):
    db = sqlite3.connect('server.db')
    sql = db.cursor()
    sql.execute(f"UPDATE orders SET Status='{status}' WHERE OrderId='{order_id}'")
    db.commit()
