class Item:
    name = None
    price = None
    count = None

    def __init__(self, name, price, count):
        self.name = name
        self.price = price
        self.count = count

    '''
        Prints item's info
    '''

    def print(self):
        print(self.name)
        print("Стоимость: " + str(self.price))
        print("Количество на складе: " + str(self.count))
