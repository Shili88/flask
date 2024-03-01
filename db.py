import os 
import json 

class Database:
    def __init__(self, name, data_dir="db_data"):
        if not os.path.exists(data_dir):
            os.makedirs(data_dir)
        self.data_dir = data_dir
        self.db_file = os.path.join(data_dir, name)

    
    def load_inventory(self):
        with open (self.db_file) as f:
            inventory = json.load(f)["inventory"]
            return inventory

    def load_history(self):
        with open (self.db_file) as f:
            history = json.load(f)["history"]
            return history
    
    def load_balance(self):
        with open (self.db_file) as f:
            balance = json.load(f)["balance"]
            return balance
    
    def save_inventory(self, inventory):
        with open (self.db_file) as f:
            warehouse = json.load(f)
        warehouse["inventory"] = inventory
        with open (self.db_file, "w") as f:
            json.dump(warehouse, f, indent=2)

    def save_history(self, history):
        with open (self.db_file) as f:
            warehouse = json.load(f)
        warehouse["history"] = history
        with open (self.db_file, "w") as f:
            json.dump(warehouse, f)

    def save_balance(self, balance):
        with open (self.db_file) as f:
            warehouse = json.load(f)
        warehouse["balance"] = balance
        with open (self.db_file, "w") as f:
            json.dump(warehouse, f)