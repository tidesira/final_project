'''
import random

class Buyer:
    def __init__(self, budget):
        self.budget = budget
        self.quantity = 0

    def purchase(self, price, quantity):
        max_purchase = min(self.budget / price, quantity)
        purchased_quantity = random.uniform(0, max_purchase)
        self.quantity += purchased_quantity
        self.budget -= purchased_quantity * price

class Seller:
    def __init__(self, cost, initial_quantity):
        self.cost = cost
        self.quantity = initial_quantity

    def sell(self, price, quantity):
        sold_quantity = min(self.quantity, quantity)
        revenue = sold_quantity * price
        self.quantity -= sold_quantity
        return revenue

def market_simulation(num_buyers, num_sellers):
    buyers = [Buyer(random.uniform(100, 1000)) for _ in range(num_buyers)]
    sellers = [Seller(random.uniform(50, 150), random.randint(10, 100)) for _ in range(num_sellers)]
    market_price = random.uniform(80, 120)

    for _ in range(10):  # Simulate 10 rounds
        for buyer in buyers:
            buyer.purchase(market_price, random.randint(1, 5))
        for seller in sellers:
            revenue = seller.sell(market_price, random.randint(1, 5))
            market_price += revenue / sum([buyer.quantity for buyer in buyers])

    print(f"Market Price: {market_price}")

if __name__ == "__main__":
    num_buyers = 5
    num_sellers = 5
    market_simulation(num_buyers, num_sellers)

'''

import random


class Product:
    def __init__(self, name, category, unit_cost, initial_quantity):
        self.name = name
        self.category = category
        self.unit_cost = unit_cost
        self.initial_quantity = initial_quantity
        self.price = 0


class Buyer:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.cart = {}

    def purchase(self, product, quantity):
        if quantity > product.initial_quantity:
            quantity = product.initial_quantity
        cost = product.price * quantity
        if cost <= self.budget:
            self.cart[product.name] = quantity
            self.budget -= cost


class Seller:
    def __init__(self, name):
        self.name = name
        self.products = []


# Define product categories and their parameters
product_categories = {
    "Electronics": (10, 100),
    "Clothing": (5, 200),
    "Books": (3, 300)
}

# Create products based on user input
products = []
for category, (unit_cost, initial_quantity) in product_categories.items():
    for i in range(2):
        product_name = input(f"Enter a name for the {category} product {i + 1}: ")
        unit_cost = float(input(f"Enter the unit cost for {product_name}: "))
        initial_quantity = int(input(f"Enter the initial quantity for {product_name}: "))
        product = Product(product_name, category, unit_cost, initial_quantity)
        products.append(product)

# Create buyers and sellers
buyers = [Buyer(f"Buyer {i + 1}", random.randint(100, 300)) for i in range(3)]
sellers = [Seller(f"Seller {i + 1}") for i in range(2)]

# Initialize product prices and quantities for sellers based on user input
for seller in sellers:
    for product in products:
        price = float(input(f"Enter the price for {product.name} from {seller.name}: "))
        quantity = int(input(f"Enter the quantity of {product.name} {seller.name} wants to sell: "))
        seller.products.append((product, price, quantity))

# Initialize buyer prices and quantities based on user input
for buyer in buyers:
    for product in products:
        price = float(input(f"Enter the price at which {buyer.name} wants to buy {product.name}: "))
        quantity = int(input(f"Enter the quantity of {product.name} {buyer.name} wants to buy: "))
        buyer.purchase(product, quantity)

# Simulate market interactions
iterations = 50
for i in range(iterations):
    for product in products:
        total_demand = sum(budget // product.price for budget in (buyer.budget for buyer in buyers))
        total_supply = sum(sum(quantity for _, _, quantity in seller.products if product == _) for seller in sellers)

        if total_demand == 0 or total_supply == 0:
            continue  # Skip if no demand or supply for this product

        product.price = product.unit_cost * (1 + random.uniform(0.1, 0.3))

        if total_demand > total_supply:
            product.price *= random.uniform(1.01, 1.1)
        elif total_supply > total_demand:
            product.price *= random.uniform(0.9, 0.99)

        for buyer in buyers:
            buyer.purchase(product, random.randint(0, 5))

    # Print market status at the end of each iteration
    print(f"Iteration {i + 1}")
    for product in products:
        print(f"{product.name} - Price: ${product.price:.2f}, Initial Quantity: {product.initial_quantity}")
    for buyer in buyers:
        print(f"{buyer.name} - Budget: ${buyer.budget:.2f}, Cart: {buyer.cart}")
    for seller in sellers:
        print(
            f"{seller.name} - Products: {[(product.name, price, quantity) for product, price, quantity in seller.products]}")
    print("-" * 50)

