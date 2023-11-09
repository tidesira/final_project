import tkinter as tk
import random
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import time

# Define the time step duration (e.g., 1 hour)
time_step_duration = 1  # 1 hour

# Initialize simulated time
simulated_time = 0

# Model parameters
initial_buyers = 100
initial_sellers = 100
max_price = 100
min_price = 10
external_shock_probability = 0.1

# Lists to store data for plotting
prices = []
supply = []
demand = []

class Buyer:
    def __init__(self, money, demand):
        self.money = money
        self.demand = demand

    def buy(self, seller):
        price = random.uniform(min_price, max_price)
        if seller.price <= price and self.money >= price:
            self.money -= price
            seller.money += price
            self.demand -= 1

class Seller:
    def __init__(self, money):
        self.money = money
        self.price = random.uniform(min_price, max_price)

    def sell(self, buyer):
        if buyer.demand >= 1 and buyer.money >= self.price:
            self.money += self.price
            buyer.money -= self.price
            buyer.demand -= 1

class MarketModel:
    def __init__(self, n_buyers, n_sellers):
        self.buyers = [Buyer(random.uniform(100, 200), random.uniform(1, 5)) for _ in range(n_buyers)]
        self.sellers = [Seller(random.uniform(100, 200)) for _ in range(n_sellers)]

    def external_shock(self):
        if random.random() < external_shock_probability:
            for seller in self.sellers:
                seller.price = random.uniform(min_price, max_price)

    def get_market_data(self):
        market_prices = [seller.price for seller in self.sellers]
        supply_count = len([price for price in market_prices if price <= max_price])
        demand_count = sum(buyer.demand for buyer in self.buyers)
        return supply_count, demand_count
    
def initialize_model():
    global model
    model = MarketModel(initial_buyers, initial_sellers)

def update_plot():
    line.set_data(range(len(prices)), prices)  # Update the plot's data
    ax.relim()  # Recompute the data limits
    ax.autoscale_view()  # Automatically adjust the plot's view
    canvas.draw()  # Redraw the canvas


def step_simulation():
    global simulated_time
    buyer = random.choice(model.buyers)
    seller = random.choice(model.sellers)
    buyer.buy(seller)
    simulated_time += time_step_duration  # Update simulated time
    if simulated_time % 10 == 0:  # Simulate an external shock every 10 hours
        model.external_shock()
    supply_count, demand_count = model.get_market_data()
    prices.append(seller.price)
    supply.append(supply_count)
    demand.append(demand_count)
    update_plot()
    formatted_price = "{:.2f}".format(seller.price)
    current_price_label.config(text="Current Price: $" + formatted_price)
    if running:  # Schedule the next step only if the simulation is running
        root.after(500, step_simulation)


def update_buyers_and_sellers():
    try:
        new_buyer_count = int(num_buyers_entry.get())
        new_seller_count = int(num_sellers_entry.get())
        if new_buyer_count >= 0 and new_seller_count >= 0:
            global initial_buyers, initial_sellers
            initial_buyers = new_buyer_count
            initial_sellers = new_seller_count
            initialize_model()  # Reset the model with the new counts
            update_labels()
            update_plot()
            error_label.config(text="")  # Clear any previous error message
        else:
            # Display an error message in the GUI if input is invalid
            error_label.config(text="Please enter non-negative integer values for buyers and sellers.")
    except ValueError:
        # Display an error message in the GUI if input cannot be converted to integers
        error_label.config(text="Invalid input. Please enter integer values for buyers and sellers.")

           

def run_simulation():
    global running
    running = True
    run_button.config(state=tk.DISABLED)  # Disable the "Run" button
    step_button.config(state=tk.DISABLED)  # Disable the "Step" button
    stop_button.config(state=tk.NORMAL)  # Enable the "Stop" button
    step_simulation()  # Start the simulation
    current_price_label.config(text="Running...")

def stop_simulation():
    global running
    running = False
    run_button.config(state=tk.NORMAL)  # Enable the "Run" button
    step_button.config(state=tk.NORMAL)  # Enable the "Step" button
    stop_button.config(state=tk.DISABLED)  # Disable the "Stop" button
    current_price_label.config(text="Simulation Stopped")

def update_labels():
    num_buyers = len(model.buyers)
    num_sellers = len(model.sellers)
    buyers_label.config(text="Buyers: " + str(num_buyers))
    sellers_label.config(text="Sellers: " + str(num_sellers))
    root.update()


# Initialize the Tkinter GUI
root = tk.Tk()
root.title("Market Simulation")

error_label = tk.Label(root, text="", fg="red")  # Create an error label with red text
error_label.pack()


buyers_label = tk.Label(root, text="Buyers: ")
sellers_label = tk.Label(root, text="Sellers: ")
buyers_label.pack()
sellers_label.pack()

step_button = tk.Button(root, text="Step", command=step_simulation)
step_button.pack()

run_button = tk.Button(root, text="Run", command=run_simulation)
run_button.pack()

stop_button = tk.Button(root, text="Stop", command=stop_simulation, state=tk.DISABLED)
stop_button.pack()

current_price_label = tk.Label(root, text="Current Price: $10")
current_price_label.pack()

# Create input fields for the number of buyers and sellers
num_buyers_label = tk.Label(root, text="Enter number of buyers:")
num_buyers_label.pack()
num_buyers_entry = tk.Entry(root)
num_buyers_entry.insert(0, str(initial_buyers))
num_buyers_entry.pack()

num_sellers_label = tk.Label(root, text="Enter number of sellers:")
num_sellers_label.pack()
num_sellers_entry = tk.Entry(root)
num_sellers_entry.insert(0, str(initial_sellers))
num_sellers_entry.pack()

update_button = tk.Button(root, text="Update Buyers and Sellers", command=update_buyers_and_sellers)
update_button.pack()

# Create a Matplotlib figure for the price plot
fig, ax = plt.subplots()
ax.set_xlabel("Time Steps")
ax.set_ylabel("Price")
line, = ax.plot(prices, label="Price")

# Create a canvas for the Matplotlib figure
canvas = FigureCanvasTkAgg(fig, master=root)
canvas_widget = canvas.get_tk_widget()
canvas_widget.pack()

# Initialize the model
model = MarketModel(initial_buyers, initial_sellers)

# Run the Tkinter main loop
running = False
root.mainloop()


