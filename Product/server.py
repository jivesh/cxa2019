from flask import Flask, render_template, request
import sqlite3

def open_DB(db):
    connection = sqlite3.connect(db)
    connection.row_factory = sqlite3.Row
    return connection

app = Flask("__name__")

@app.route("/")
def root():
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

if __name__ == "__main__":
    app.run()