from flask import Flask, render_template, request
import sqlite3
import os
import shutil
import time
import random

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
@app.route("/classify", methods=["GET"])
def classify():
    time.sleep(0.1)
    # TODO: check working on local server with flask
    # run the deep learning model and make prediction of the classification
    os.system('python3 final_garbage.py')
    # TODO: play animation of the classification process
    result = open("prediction.txt", "r")
    for line in result:
        result_str = line
    final_url = result_str + ".html"
    return render_template(final_url)
    
@app.route("/reward", methods=["GET"])
def reward():
    # TODO: trigger reward system when mistakes were spotted

    # # TODO: move the image to trash folder and update the counter
    # # os.remove("demofile.txt")
    # random_number = random.randint(1,100001)
    # random_name = "/Users/ue/Downloads/CXA2019/cxa2019/Product/static/images/trash/trash" + str(random_number) + ".png"
    # shutil.move("/Users/ue/Downloads/CXA2019/cxa2019/Product/static/images/downloaded_images/trash.png",
    #             random_name)
    # TODO: display ending page
    # return render_template("")
    return "Hey"



if __name__ == "__main__":
    app.run()