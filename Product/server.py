from flask import Flask, render_template, request
import sqlite3
import os
import shutil
# shutil.move("path/to/current/file.foo", "path/to/new/destination/for/file.foo")

def open_DB(db):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    return connection

app = Flask("__name__")

@app.route("/")
def root():
    # TODO: UI to be updated
    return render_template("camera.html")

@app.route("/addUser", methods=["POST"])
def add_user():
    # the function is to create a new user
    con = open_DB('user.db')
    try:
        user_name = request.form['name']
        con.execute("INSERT INTO User (Name, Points) VALUES(?, ?)", (user_name, 0))
        con.commit()
    except:
        print("Database error")
    con.close()
    # TODO: supposed to render a certain page 
    return render_template("products.html")

# triggered after clicking the snap button in the camera page
@app.route("/classify_page", methods=["POST"])
def classify():
    # TODO: shift the image to specific folder
    # TODO: run the deep learning model 
    # TODO: make prediction of the classification
    # TODO: play animation of the classification process
    # TODO: trigger reward system when mistakes were spotted
    # TODO: move the image to trash folder
    # TODO: display ending page
    return render_template("")



if __name__ == "__main__":
    app.run()