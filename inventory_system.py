"""
inventory_system.py

A simple inventory management system module.

This module allows for adding, removing, and querying item quantities in an
in-memory stock inventory. It also supports saving the inventory to and
loading it from a JSON file.
"""

import json
from datetime import datetime


def add_item(stock_data, item="default", qty=0, logs=None):
    """
    Adds a specified quantity of an item to the stock.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to add.
        qty (int or float): The quantity to add.
        logs (list, optional): A list to append log messages to.
                               Defaults to None.
    """
    if logs is None:
        logs = []

    # Basic input validation
    if not isinstance(item, str) or not item:
        print(f"Error: Item name '{item}' is not a valid string.")
        return
    if not isinstance(qty, (int, float)):
        print(f"Error: Quantity '{qty}' for item '{item}' is not a number.")
        return
    if qty < 0:
        print(f"Warning: Adding negative quantity ({qty}) for '{item}'.")

    stock_data[item] = stock_data.get(item, 0) + qty
    # Use modern f-string for formatting
    logs.append(f"{str(datetime.now())}: Added {qty} of {item}")


def remove_item(stock_data, item, qty):
    """
    Removes a specified quantity of an item from the stock.

    If the quantity drops to 0 or below, the item is removed from the
    inventory.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to remove.
        qty (int or float): The quantity to remove.
    """
    try:
        if item in stock_data:
            stock_data[item] -= qty
            if stock_data[item] <= 0:
                del stock_data[item]
        else:
            print(f"Info: Item '{item}' not in stock, cannot remove.")
    except KeyError:
        # This can happen if the item was removed by another process
        print(f"Warning: Could not remove '{item}', it was not found.")
    except TypeError:
        print(f"Error: Invalid quantity '{qty}' for item '{item}'.")


def get_qty(stock_data, item):
    """
    Gets the current quantity of a specific item.

    Args:
        stock_data (dict): The inventory dictionary.
        item (str): The name of the item to query.

    Returns:
        int or float: The quantity of the item, or 0 if not found.
    """
    return stock_data.get(item, 0)


def load_data(stock_data, file="inventory.json"):
    """
    Loads the inventory from a JSON file, updating the stock_data dict.

    Args:
        stock_data (dict): The inventory dictionary to update.
        file (str): The name of the file to load from.
    """
    try:
        with open(file, "r", encoding="utf-8") as f:
            data = json.loads(f.read())
            stock_data.clear()  # Clear existing data
            stock_data.update(data)  # Load new data
            print(f"Data loaded from {file}.")
    except FileNotFoundError:
        print(f"Warning: {file} not found. Starting with an empty inventory.")
    except json.JSONDecodeError:
        print(f"Error: Could not decode JSON from {file}.")
    except IOError as e:
        print(f"Error loading file {file}: {e}")


def save_data(stock_data, file="inventory.json"):
    """
    Saves the current inventory to a JSON file.

    Args:
        stock_data (dict): The inventory dictionary to save.
        file (str): The name of the file to save to.
    """
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
            print(f"Data saved to {file}.")
    except IOError as e:
        print(f"Error saving file {file}: {e}")


def print_data(stock_data):
    """
    Prints a report of all items and their quantities.

    Args:
        stock_data (dict): The inventory dictionary to print.
    """
    print("\n--- Items Report ---")
    if not stock_data:
        print("Inventory is empty.")
    else:
        for item, qty in stock_data.items():
            print(f"{item} -> {qty}")
    print("--------------------\n")


def check_low_items(stock_data, threshold=5):
    """
    Finds all items with a quantity below the threshold.

    Args:
        stock_data (dict): The inventory dictionary.
        threshold (int): The quantity threshold.

    Returns:
        list: A list of item names below the threshold.
    """
    return [item for item, qty in stock_data.items() if qty < threshold]


def main():
    """
    Main function to run the inventory management simulation.
    """
    stock_data = {}  # Initialize a local dictionary
    logs = []        # Initialize a local log list

    # Load initial data (if any)
    load_data(stock_data)

    # Perform operations, passing the state
    add_item(stock_data, "apple", 10, logs)
    add_item(stock_data, "banana", 5, logs)
    
    # These invalid calls will now be handled gracefully
    add_item(stock_data, "banana", -2, logs)
    add_item(stock_data, 123, "ten", logs)

    remove_item(stock_data, "apple", 3)
    remove_item(stock_data, "orange", 1)  # Item not in stock

    print("Apple stock:", get_qty(stock_data, "apple"))
    print("Orange stock:", get_qty(stock_data, "orange"))

    print("Low items:", check_low_items(stock_data))

    print_data(stock_data)
    save_data(stock_data)

    print("\nLogs:")
    for log_entry in logs:
        print(log_entry)


if __name__ == "__main__":
    main()

