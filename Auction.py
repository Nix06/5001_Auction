from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from datetime import timedelta


app = Flask(__name__)
app.secret_key = "password" #used to sign session cookies for protection against cookie data tampering
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.permanent_session_lifetime = timedelta(minutes= 5) #means session holds the data for the specified amount of time

db = SQLAlchemy(app)

class User(db.model):   #Creates a class used to create a table in the database for the users to login
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(50))
    password = db.Column(db.String(50))

class Items(db.model):  #Creates a class used to create a table in the database for the users to put a item
    id = db.colmn(db.Integer, primary_key = True)
    item_nm = db.Column(db.String(50))
    item_des = db.Column(db.String(100))

@app.route("/")
def home():
    return render_template ("home.html")  

@app.route("/sell_new_item", methods = ["POST", "GET"]) #use the POST method for when we want to transfer the data securley and the GET method for when the data doesnt need to be secure
def sell():
    if request.method == "POST":
        name = request.form ["item_nm"]   #gives the variable name whatever the user inputted the items name as
        description = request.form ["item_des"] #gives the variable description whatever the user inputted the item description as
        sell_data = Items(name, description)    #Creates an object so can be inputted into database
        db.session.add(sell_data)   #Adds the object into the database
        db.session.commit()     #Commits the changes made to the database

    else:
        return render_template ("sell.html")

@app.route("/my_items")
def items():
    return render_template ("items.html")

@app.route("/login")
def login():
    return render_template ("login.html")

@app.route("/logout")
def logout():
    return render_template ("logout.html")

@app.route("/create")
def create():
    return render_template ("create.html")

if __name__ == "__main__":
    app.run(debug=True)

