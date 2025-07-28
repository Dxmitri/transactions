import hashlib
import time
import datetime
import json

class Block:
    def __init__(self, index, timestamp, transaction, previous_hash=''):
        self.index = index
        self.timestamp = timestamp
        self.transaction = transaction
        self.previous_hash = previous_hash
        self.hash = self.compute_hash()

    def compute_hash(self):
        block_string = f"{self.index}{self.timestamp}{self.transaction}{self.previous_hash}"
        return hashlib.sha256(block_string.encode()).hexdigest()

class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]

    def create_genesis_block(self):
        return Block(0, time.time(), "Genesis Block", "0")

    def get_last_block(self):
        return self.chain[-1]

    def add_transaction(self, transaction):
        prev_block = self.get_last_block()
        new_block = Block(len(self.chain), time.time(), transaction, prev_block.hash)
        self.chain.append(new_block)

    def print_chain(self):
        for block in self.chain:
            print(f"Index: {block.index}")
            print(f"Timestamp: {time.ctime(block.timestamp)}")
            print(f"Transaction: {block.transaction}")
            print(f"Hash: {block.hash}")
            print(f"Previous Hash: {block.previous_hash}")
            print("-" * 50)

def display_items(items):
    print("\n{:<15} | {:<10} | {:<5} | {:<10}".format("Snacks", "Price(Rs)", "ID", "Quantity"))
    print("-" * 50)
    for id, item in items.items():
        if item['category'] == 'Snacks':
            print("{:<15} | {:<10} | {:<5} | {:<10}".format(item['name'], item['price'], id, item['quantity']))

    print("\n{:<15} | {:<10} | {:<5} | {:<10}".format("Beverages", "Price(Rs)", "ID", "Quantity"))
    print("-" * 50)
    for id, item in items.items():
        if item['category'] == 'Beverages':
            print("{:<15} | {:<10} | {:<5} | {:<10}".format(item['name'], item['price'], id, item['quantity']))

def process_purchase(items, blockchain):
    try:
        money = int(input("Enter your money in (RS):"))
        if not 50 <= money <= 200:
            print("Your money wasn't accepted")
            print("your refund is : Rs", money)
            return

        item_id = int(input("Enter the ID of the item that you want :"))
        if item_id not in items:
            print("You have inserted a wrong ID")
            print("Your refund is :Rs", money)
            return

        quantity = int(input("Enter the quantity that you want :"))
        confirm = int(input("Enter 1 to confirm your purchase or enter 2 to exit :"))

        if confirm == 1:
            item = items[item_id]
            if quantity > item["quantity"]:
                print("There is not enough product available")
                print("Your refund is", money)
                return

            price = item["price"] * quantity
            if price > money:
                print("You don't have enough money")
                print("Your refund is", money)
                return

            item["quantity"] -= quantity
            change = money - price
            print(f"You have selected {quantity} {item['name']}")
            print(f"Your change is :Rs {change}")

            blockchain.add_transaction({
                "item": item["name"],
                "quantity": quantity,
                "paid": money,
                "change": change,
                "date": str(datetime.datetime.now())
            })
            with open('transactions.json', 'r+') as f:
                try:
                    data = json.load(f)
                except json.JSONDecodeError:
                    data = []
                data.append({
                    "item": item["name"],
                    "quantity": quantity,
                    "paid": money,
                    "change": change,
                    "date": str(datetime.datetime.now())
                })
                f.seek(0)
                json.dump(data, f, indent=4)
        elif confirm == 2:
            print("You have exited vending machine")
            print("Your refund is :Rs", money)
        else:
            print("You have entered a wrong command")
            print("Your refund is :Rs", money)

    except ValueError:
        print("Invalid input. Please enter a number.")

def admin_menu(items, blockchain):
    try:
        password = int(input("Enter admin password: "))
        if password != 1234:
            print("Wrong password.")
            return
    except ValueError:
        print("Invalid password.")
        return

    while True:
        print("\n1. Add new product")
        print("2. Update existing product/delete product")
        print("3. List all products")
        print("4. View transaction log for purchases")
        print("5. Exit admin menu")
        
        try:
            choice = int(input("Enter the number for the action that you want to execute: "))
            if choice == 1:
                name = input("Enter the name of the new product: ")
                id = int(input("Enter the ID of the product to add: "))
                price = int(input("Enter the price of the new product: "))
                quantity = int(input("Enter the quantity of the new product: "))
                category = input("Enter the category (Snacks/Beverages): ")
                items[id] = {"name": name, "price": price, "quantity": quantity, "category": category}
                print("Product added successfully.")
                display_items(items)
            elif choice == 2:
                update_delete = int(input("Enter 1 to update product and enter 2 to delete product: "))
                if update_delete == 1:
                    id = int(input("Enter the id of the product that you want to update: "))
                    if id in items:
                        price = int(input("Enter the new price of the product: "))
                        quantity = int(input("Enter the new quantity of product: "))
                        items[id]["price"] = price
                        items[id]["quantity"] = quantity
                        print("Product updated successfully.")
                    else:
                        print("Product not found.")
                elif update_delete == 2:
                    id = int(input("Enter the ID of the product that you want to delete: "))
                    if id in items:
                        del items[id]
                        print("Product deleted successfully.")
                    else:
                        print("Product not found.")
                else:
                    print("You have entered a wrong command.")
            elif choice == 3:
                display_items(items)
            elif choice == 4:
                blockchain.print_chain()
            elif choice == 5:
                break
            else:
                print("You have inserted a wrong command.")
        except ValueError:
            print("Invalid input. Please enter a number.")

def student_menu(items, blockchain):
    print("\n1. List all products")
    print("2. Purchase a product")
    
    try:
        choice = int(input("Enter a number for the command that you want to execute: "))
        if choice == 1:
            display_items(items)
        elif choice == 2:
            process_purchase(items, blockchain)
        else:
            print("You have entered a wrong command.")
    except ValueError:
        print("Invalid input. Please enter a number.")

def main():
    items = {
        41: {"name": "Snickers", "price": 45, "quantity": 4, "category": "Snacks"},
        42: {"name": "Slai o'lai", "price": 25, "quantity": 6, "category": "Snacks"},
        43: {"name": "Sando", "price": 18, "quantity": 3, "category": "Snacks"},
        44: {"name": "Kinder", "price": 18, "quantity": 2, "category": "Snacks"},
        45: {"name": "Kit-kat", "price": 45, "quantity": 5, "category": "Snacks"},
        46: {"name": "Oreo", "price": 23, "quantity": 2, "category": "Snacks"},
        31: {"name": "Fuse Tea", "price": 50, "quantity": 3, "category": "Beverages"},
        32: {"name": "Coca-cola", "price": 55, "quantity": 5, "category": "Beverages"},
        33: {"name": "Water", "price": 22, "quantity": 6, "category": "Beverages"},
        34: {"name": "White Mirinda", "price": 42, "quantity": 2, "category": "Beverages"},
        35: {"name": "Pink Mirinda", "price": 42, "quantity": 7, "category": "Beverages"},
        36: {"name": "Sprite", "price": 55, "quantity": 2, "category": "Beverages"},
    }
    blockchain = Blockchain()

    print()
    print("Welcome to polytechnics vending machince !")
    print("\nMinimun money accpeted by the machine is Rs50")
    print("Maximun money accepted by the machine is Rs200")

    display_items(items)
    while True:
        try:
            role = int(input("\nEnter 1 for Admin & 2 for Student (or 0 to exit): "))
            if role == 1:
                admin_menu(items, blockchain)
            elif role == 2:
                student_menu(items, blockchain)
            elif role == 0:
                break
            else:
                print("Invalid role selected.")
        except ValueError:
            print("Invalid input. Please enter a number.")

if __name__ == "__main__":
    main()
