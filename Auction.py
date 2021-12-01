from flask import Flask, redirect, url_for, render_template, request, session, flash
from flask_sqlalchemy import SQLAlchemy, sqlalchemy
from datetime import timedelta
import os

from sqlalchemy.orm import relationship

app = Flask(__name__)
app.secret_key = "password" #used to sign session cookies for protection against cookie data tampering
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["IMAGE_UPLOADS"] = os.path.dirname("C:\\Users\\Nick\\Documents\\Uni\\5001_Auction\\static\\images\\")  #Means the image uploaded gets stored into the images folder in the project

app.permanent_session_lifetime = timedelta(minutes = 1) #means session holds the data for the specified amount of time

db = SQLAlchemy(app)

class User(db.Model):   #Creates a class used to create a table in the database for the users to login
    id = db.Column(db.Integer, primary_key = True)  #Creates the ID column for the database and makes it the primary key
    user_name = db.Column(db.String(50))    #Creates the username column for the users database and gives it a maximum length of 50
    password = db.Column(db.String(50))     #Creates the password column for the users database and gives it a maximum length of 50

    def __init__(self, username, password): #Initalizes the database
        self.user_name = username   #Gives the objects in the database their attributes
        self.password = password


class Items(db.Model):  #Creates a class used to create a table in the database for the users to put a item
    id = db.Column(db.Integer, primary_key = True)     #Creates the ID column for the database and makes it the primary key
    item_nm = db.Column(db.String(50))      #Creates the item name column for the item database and gives it a maximum length of 50
    item_des = db.Column(db.String(100))    #Creates the item description column for the item database and gives it a maximum length of 100
    item_img = db.Column(db.String(50))     #Creates the item image column for the item database and gives it a maximum length of 50
    item_user = db.Column(db.String(50))    #Creates the item user column for the item database and gives it a maximum length of 50

    def __init__(self, itemname, itemdes, item_img, item_user): #Initalizes the database
        self.item_nm = itemname     #Gives the objects in the database their attributes
        self.item_des = itemdes
        self.item_img = item_img
        self.item_user = item_user

db.create_all()     #Creates the database

@app.route("/")
def home():
    return render_template ("home.html", values=Items.query.all()) #querys all the vinformation in the datbase and gives the variable values the information

@app.route("/sell", methods = ["POST", "GET"]) #use the POST method for when we want to transfer the data securley and the GET method for when the data doesnt need to be secure
def sell():
    if "User" in session: #This checks to see if a user is in the session (so is logged in)
        if request.method == "POST":
            item_name = request.form ["item_nm"]   #gives the variable name whatever the user inputted the items name as
            item_description = request.form ["item_des"] #gives the variable description whatever the user inputted the item description as
            if request.files:   #This if statement runs so the image uploaded can be put into the image folder
                item_img = request.files['item_img']        #Gives the variable item_img the value of what ever picture the user picks when they click the button
                print(item_img.filename)    #Prints out the file name on the website for the user to see
                item_img.save(os.path.join(app.config["IMAGE_UPLOADS"], item_img.filename))     #Saves the image to the images folder
                flash("Image saved", "info")       #Flashes the user a message to let them know their image was saved
                sell_data = Items(item_name, item_description, item_img.filename, session['User'])    #Creates an object so can be inputted into database
                db.session.add(sell_data)   #Adds the object into the database
                db.session.commit()     #Commits the changes made to the database
            else:
                flash("Please upload an image!")    #If the user doesnt upload a image they get flashed this message

        return render_template("sell.html")
    else:
        flash("Please login to add an item")    #If the user is not logged in (not in the session) then they will be asked to login before uploading an image
        return render_template("sell.html")

@app.route("/items")
def items():
    if session:     #Uses the if statement to see if a user is logged in (in session)
        user = session['User']      #Gives the variable user the username for whoever is in the session)
        return render_template("items.html", values = Items.query.filter_by(item_user = user).all())       #Returns the item template and querys the database for all the information for the current user and gives the information to the variable value
    else:
        flash("You are not logged in", "info")
        return redirect(url_for('home'))    #Sends the user back to the homepage if they are not logged in

@app.route("/login", methods = ["POST", "GET"])
def login():
    if request.method == "POST":
        if session:     #Checks to see if the User is logged in already
            flash("You are already logged in", "info")
            return redirect(url_for('login'))
        else:
            session.permanent = True    #Makes the session cookies permanent after the user has logged in
            user = request.form["usr_name"]     #Gives the variable user the information inputted
            found_user = User.query.filter_by(user_name=user).first()   #Querys the database finding if the input matches any username in the database
            if found_user:
                passw = request.form["usr_password"]    #Gives the variable passw the input put into the password form
                if found_user.password == passw:    #Compares the found usernames password to the password inputted
                    session["User"] = user       #Creates a session for the logged in user
                    flash("You are logged in", "info")
                    return redirect(url_for('home'))
                else:
                    flash("Incorrect password", "info")     #If the password is wrong then the user gets flashed a message saying this
                    return redirect(url_for('login'))

            else:
                flash("Username not found", "info")     #If the username is incorrect then the user gets flashed a message saying this
                return redirect(url_for('login'))


    return render_template ("login.html")

@app.route("/logout")
def logout():
    session.pop("User", None)       #Removes the user from the session when they log out
    flash("You have been logged out", "info")
    return render_template("logout.html")
 

@app.route("/create", methods = ["POST", "GET"])
def create():
    if request.method == "POST":
        username = request.form ["usr_name"]    #Gives the variable username the inputted values for the username form
        new_password = request.form ["usr_password"]    #Gives the variable new_password the inputted values for the password form
        create_user = User(username, new_password)      #Makes the object create user and gives it the attributes for username and password
        db.session.add(create_user)     #Adds the object to the database
        db.session.commit()     #Commits the changes
    flash("You have created an account", "info")
    return render_template ("create.html")


if __name__ == "__main__":
    app.run(debug=True)

