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

        for seller in self.sellers:
            seller.price = max(min(seller.price, max_price), min_price)

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
    if prices:
        ax.set_ylim(min(min_price, min(prices)), max(max_price, max(prices)))  # Set y-axis limits to the max price range
    else:
        ax.set_ylim(min_price, max_price)  # Set y-axis limits to the default price range
    canvas.draw()  # Redraw the canvas


def step_simulation():
    global simulated_time
    buyer = random.choice(model.buyers)
    seller = random.choice(model.sellers)
    # Generate a candidate price within the current specified range
    candidate_price = random.uniform(min_price, max_price)

    # Ensure the candidate price is within the range, adjusting if necessary
    seller.price = max(min(candidate_price, max_price), min_price)

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


def update_parameters():
    try:
        new_external_shock_prob = float(external_shock_entry.get())
        new_min_price = float(min_price_entry.get())
        new_max_price = float(max_price_entry.get())
        if 0 <= new_external_shock_prob <= 1 and new_min_price < new_max_price:
            global external_shock_probability, min_price, max_price
            external_shock_probability = new_external_shock_prob
            min_price = new_min_price
            max_price = new_max_price
            error_label.config(text="")
        else:
            # Display an error message in the GUI if input is invalid
            error_label.config(text="Invalid input. Please check parameter values.")
    except ValueError:
        # Display an error message in the GUI if input cannot be converted to floats
        error_label.config(text="Invalid input. Please enter valid numerical values for parameters.")       


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

current_price_label = tk.Label(root, text="Current Price: $0")
current_price_label.pack()

# Left Frame for Buyers and Sellers
left_frame = tk.Frame(root)
left_frame.pack(side=tk.LEFT, padx=10)

# Create input fields for additional parameters
external_shock_label = tk.Label(left_frame, text="Enter external shock probability (0 to 1):")
external_shock_label.pack()
external_shock_entry = tk.Entry(left_frame)
external_shock_entry.insert(0, str(external_shock_probability))
external_shock_entry.pack()

min_price_label = tk.Label(left_frame, text="Enter min price:")
min_price_label.pack()
min_price_entry = tk.Entry(left_frame)
min_price_entry.insert(0, str(min_price))
min_price_entry.pack()

max_price_label = tk.Label(left_frame, text="Enter max price:")
max_price_label.pack()
max_price_entry = tk.Entry(left_frame)
max_price_entry.insert(0, str(max_price))
max_price_entry.pack()


# Button to update all parameters
update_parameters_button = tk.Button(left_frame, text="Update Parameters", command=update_parameters)
update_parameters_button.pack()


# Right Frame for Additional Parameters
right_frame = tk.Frame(root)
right_frame.pack(side=tk.RIGHT, padx=10)

# Create input fields for the number of buyers and sellers
num_buyers_label = tk.Label(right_frame, text="Enter number of buyers:")
num_buyers_label.pack()
num_buyers_entry = tk.Entry(right_frame)
num_buyers_entry.insert(0, str(initial_buyers))
num_buyers_entry.pack()

num_sellers_label = tk.Label(right_frame, text="Enter number of sellers:")
num_sellers_label.pack()
num_sellers_entry = tk.Entry(right_frame)
num_sellers_entry.insert(0, str(initial_sellers))
num_sellers_entry.pack()

update_button = tk.Button(right_frame, text="Update Buyers and Sellers", command=update_buyers_and_sellers)
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


