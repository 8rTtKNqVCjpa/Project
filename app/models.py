import json
import os

chemin = r"C:\Users\hp\Desktop\Projects\projet\mock_data\csvjson.json"

def load_data():
    if os.path.exists(chemin):
        with open(chemin, "r", encoding="UTF-8") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                print('Error detected: Invalid JSON format')
                return None
            except IOError as e:
                print(f'Error detected: {e}')
                return None
    else:
        return "NO DATA FOUND"

def getorderbyid(order_id):
    data = load_data()
    for order in data:
        if order['ORDERNUMBER'] == order_id:
            return order
    return None

def getorderbystatus(order_status):
    orders = []
    data = load_data()
    for order in data:
        if order.get('STATUS') == order_status:
            orders.append(order)
    return orders if orders else None
