import json
from datetime import datetime

# No more global variable

def addItem(stock_data, item="default", qty=0, logs=None):
    if logs is None:
        logs = []
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def removeItem(stock_data, item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Item not in stock, do nothing
        pass

def getQty(stock_data, item):
    # Use .get() for safety, returning 0 if item not found
    return stock_data.get(item, 0) 

def loadData(stock_data, file="inventory.json"):
    # No global statement
    try:
        with open(file, "r", encoding="utf-8") as f:
            # Update the dictionary that was passed in
            loaded_data = json.loads(f.read())
            stock_data.clear()
            stock_data.update(loaded_data)
    except FileNotFoundError:
        print(f"Info: {file} not found, starting with empty inventory.")
        # No need to assign to stock_data, it's already {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. Starting with empty inventory.")
        stock_data.clear()


def saveData(stock_data, file="inventory.json"):
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
    except IOError as e:
        print(f"Error saving data to {file}: {e}")

def printData(stock_data):
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(stock_data, threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    stock_data = {} # Initialize local variable
    logs = []       # Initialize local logs
    
    # Load data first
    loadData(stock_data) 

    addItem(stock_data, "apple", 10, logs)
    addItem(stock_data, "banana", -2, logs)
    addItem(stock_data, 123, "ten", logs)  # invalid types, no check
    removeItem(stock_data, "apple", 3)
    removeItem(stock_data, "orange", 1)
    
    print("Apple stock:", getQty(stock_data, "apple"))
    print("Low items:", checkLowItems(stock_data))
    
    saveData(stock_data)
    # loadData(stock_data) # Not really needed to load after saving
    printData(stock_data)
    
    print("\nLogs:")
    for log in logs:
        print(log)

# Add if __name__ == "__main__": guard
if __name__ == "__main__":
    main()
