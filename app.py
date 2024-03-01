from flask import Flask
from flask import render_template
from flask import request
from flask import redirect
from flask import flash
from flask import url_for

from db import Database
import db

app = Flask(__name__)
app.config["SECRET_KEY"] = "mysecretkey"

db = Database(name="warehouse.json")

"""Daily Warehouse APP;

Current stock & balance

sale
purchase
balance
history
"""

@app.route("/")
def index ():
    inventory = db.load_inventory()
    balance = db.load_balance()
    return render_template ("index.html", item_name=inventory, inventory=inventory, balance=balance)


@app.route("/purchase", methods=["get", "post"])
def purchase ():
    if request.method == "POST":
        print(request.form)
        item_name = request.form["item_name"]
        item_quantity = int(request.form["item_quantity"])
        item_price = int(request.form["price"])
        purchase = item_quantity * item_price
        
        balance = db.load_balance()
        inventory = db.load_inventory()
        history = db.load_history()
    
        if balance > purchase:
            balance -= purchase
            history.append("Item bought into the inventory: {} Quantity: {} Price per unit: {}".format(item_name, item_quantity, item_price))
            if item_name not in inventory:
                inventory[item_name]= {
                    "item_quantity": item_quantity,
                    "item_price": item_price
                }
                history.append("New product added into inventory: {} Quantity: {} Price per unit: {}".format(item_name, item_quantity, item_price))
            else:
                inventory[item_name]["item_quantity"] += item_quantity
                balance -= purchase
                history.append("stock added for item: {} Quantity: {} Price: {}".format(item_name, item_quantity, item_price))
            flash(f"Purchase{item_name} succesfully!")
        else:
            flash ("No enough balance in the account!")

        db.save_balance(balance)
        db.save_history(history)
        db.save_inventory(inventory)
        
        return redirect(url_for("index"))
    return render_template ("purchase.html")


@app.route("/sale", methods=["get", "post"])
def sale ():
    if request.method == "POST":
        print(request.form)
        item_name = request.form["item_name"]
        item_quantity = int(request.form["item_quantity"])
        item_price = int(request.form["price"])
        sale = item_quantity * item_price
        
        balance = db.load_balance()
        inventory = db.load_inventory()
        history = db.load_history()


        if item_name in inventory:
            inventory[item_name] = {"item_quantity": 0.0, "item_quantity": 0}
            history.append("Sold Item: {} Quantity: {} Price: {}".format(item_name, item_quantity, item_price))
            if inventory[item_name]["item_quantity"] < item_quantity:
                flash(f"Current item {item_name} not enough to sale.")
            else:
                inventory[item_name] -= item_quantity
                balance += sale
                flash(f"Transaction for {item_name} succesfully.")
                history.append("Sold Item: {} Quantity: {} Price: {}".format(item_name, item_quantity, item_price))
        else:
            flash(f"Currrent {item_name} does not available.")

        db.save_balance(balance)
        db.save_history(history)
        db.save_inventory(inventory)
        
        return redirect(url_for("index"))
    return render_template ("sale.html")

@app.route("/balance", methods=["get", "post"])
def balance ():
    if request.method == "POST":
        print(request.form)
        balance_action = request.form["balance_action"]
        amount = int(request.form["amount"])
        
        balance = db.load_balance()
        inventory = db.load_inventory()
        history = db.load_history()

        if balance_action == "Add":
            balance += amount 
            history.append("Function {}, Amount {}" .format(balance_action, amount))
            flash(f"Successfully added to the account")
        elif balance_action == "Subtract":
            if amount >= balance:
                flash("Not enough the money to subtract")
            else: 
                balance -= amount 
                history.append("Function {}, Amount {}" .format(balance_action, amount))
                flash(f"Successfully dedcuted from the account")     
        else:
            flash (f"The function {balance_action} is not available.")                  

        db.save_balance(balance)
        db.save_history(history)
        db.save_inventory(inventory)
        return redirect(url_for("index"))
    return render_template ("balance.html")

@app.route("/history" , methods=["get", "post"])
def history ():
    history = db.load_history()
    return render_template ("history.html", history=history)

