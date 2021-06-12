class Catalog:
    items = []

    def __init__(self, items):
        self.items = items

    '''
        Returns item by name 
    '''
    def get_item(self, name):
        for item in self.items:
            if item.name == name:
                return item
        return None

    '''
        Edits price of item in catalog
    '''
    def edit_item_price(self, name, new_price):
        for item in self.items:
            if item.name == name:
                item.price = new_price
                return True

        return False

    '''
        Edits count of items in catalog 
    '''
    def edit_item_count(self, name, new_count):
        for item in self.items:
            if item.name == name:
                item.price = new_count
                return True

        return False

    '''
        Prints all items from catalog
    '''
    def print(self):
        print("Данный каталог состоит из следующих товаров:")
        for item in self.items:
            item.print()
            print()
