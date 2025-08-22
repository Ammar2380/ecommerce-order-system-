import csv
from datetime import datetime


def log(message):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("log.txt", "a") as f:
        f.write(f"[{now}] {message}\n")


def get_product(product_id):
    with open("Product.csv", newline="") as file:
        reader = csv.DictReader(file)
        for row in reader:
            if int(row["id"]) == product_id:
                return row["name"], int(row["price"])
    return None, None


class Order:
    discount = 0 

    def __init__(self):
        self.items = [] 

    
    def log_action(func):
        def wrapper(self, *args, **kwargs):
            result = func(self, *args, **kwargs)
            log(f"Executed {func.__name__}")
            return result
        return wrapper

  
    @log_action
    def add_item_by_id(self, product_id, quantity):
        if not Order.is_valid_product_id(product_id):
            return

        name, price = get_product(product_id)
        total = price * quantity
        self.items.append((name, quantity, total))
        log(f"Added item: {name} (x{quantity}) - Total: {total}")
        print(f"Added {name} x{quantity} - Total: {total}")

    @log_action
    def calculate_total(self):
        subtotal = sum(item[2] for item in self.items)
        total = subtotal * (1 - Order.discount / 100)
        log(f"Calculated total with discount: {total}")
        print(f"Total after {Order.discount}% discount: {total}")
        return total


    @classmethod
    def set_discount(cls, discount_rate):
        cls.discount = discount_rate
        log(f"Discount set to {discount_rate}%")
        print(f"Discount set to {discount_rate}%")

  
    @staticmethod
    def is_valid_product_id(product_id):
        name, price = get_product(product_id)
        if name is None:
            log(f"Invalid product ID attempt: {product_id}")
            print(f"Invalid product ID: {product_id}")
            return False
        return True


if __name__ == "__main__":
    my_order = Order()

   
    my_order.add_item_by_id(1, 2,4)  
    my_order.add_item_by_id(4, 3)  


    my_order.add_item_by_id(99, 1)  

  
    Order.set_discount(10)

  
    my_order.calculate_total()
