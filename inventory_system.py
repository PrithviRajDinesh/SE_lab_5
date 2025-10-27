import json
from datetime import datetime

# Global variable
stock_data = {}

def addItem(item="default", qty=0, logs=None):
    if logs is None:
        logs = []
    if not item:
        return
    stock_data[item] = stock_data.get(item, 0) + qty
    logs.append("%s: Added %d of %s" % (str(datetime.now()), qty, item))

def removeItem(item, qty):
    try:
        stock_data[item] -= qty
        if stock_data[item] <= 0:
            del stock_data[item]
    except KeyError:
        # Item not in stock, do nothing
        pass

def getQty(item):
    return stock_data[item]

def loadData(file="inventory.json"):
    global stock_data
    try:
        with open(file, "r", encoding="utf-8") as f:
            stock_data = json.loads(f.read())
    except FileNotFoundError:
        print(f"Info: {file} not found, starting with empty inventory.")
        stock_data = {}
    except json.JSONDecodeError:
        print(f"Error: Could not decode {file}. Starting with empty inventory.")
        stock_data = {}


def saveData(file="inventory.json"):
    try:
        with open(file, "w", encoding="utf-8") as f:
            f.write(json.dumps(stock_data, indent=4))
    except IOError as e:
        print(f"Error saving data to {file}: {e}")

def printData():
    print("Items Report")
    for i in stock_data:
        print(i, "->", stock_data[i])

def checkLowItems(threshold=5):
    result = []
    for i in stock_data:
        if stock_data[i] < threshold:
            result.append(i)
    return result

def main():
    addItem("apple", 10)
    addItem("banana", -2)
    addItem(123, "ten")  # invalid types, no check
    removeItem("apple", 3)
    removeItem("orange", 1)
    print("Apple stock:", getQty("apple"))
    print("Low items:", checkLowItems())
    saveData()
    loadData()
    printData()

main()
