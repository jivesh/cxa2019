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
    return render_template("log_in.html")


# # TODO
# @app.route("/addUser", methods=["POST"])
# def add_user():
#     # the function is to create a new user
#     con = open_DB('user.db')
#     try:
#         user_name = request.form['name']
#         con.execute("INSERT INTO User (Name, Points) VALUES(?, ?)", (user_name, 0))
#         con.commit()
#     except:
#         print("Database error")
#     con.close()
#     # TODO: supposed to render a certain page
#     return render_template("products.html")


@app.route("/main_page", methods=["POST"])
def main_page():
    con = open_DB('user.db')
    input_name = request.form["user_name"]
    try:
        record = con.execute("SELECT Name, Points FROM User WHERE Name = \"" +
                             input_name + "\"")
        np_dict = record.fetchall()
        for line in np_dict:
            point = line["Points"]
    except:
        point = 0
        con.execute("INSERT INTO User (Name, Points) VALUES(?, ?)",
                    (input_name, point))
        con.commit()
    handle = open("current_user.txt", "w")
    handle.write(input_name)
    handle.close()
    return render_template("main_page.html", point=point)


@app.route("/throw_rubbish", methods=["POST"])
def throw_rubbish():
    return render_template("camera.html")


# triggered after clicking the snap button in the camera page
@app.route("/classify", methods=["GET"])
def classify():
    # to make sure the image saved
    time.sleep(0.1)
    # run the deep learning model and make prediction of the classification
    os.system('python3 final_garbage.py')
    # retreive the type of trash
    result = open("prediction.txt", "r")
    for line in result:
        result_str = line
    # update the count of each type of trash
    labels = {
        'cardboard': 0,
        'glass': 1,
        'metal': 2,
        'paper': 3,
        'plastic': 4,
        'trash': 5
    }
    index = labels[result_str]
    handle = open("counter.txt", "r")
    for line in handle:
        data = line.split(",")
    data[index] = str(int(data[index]) + 1)
    handle.close()
    handle = open("counter.txt", "w")
    for i in range(6):
        handle.write(data[i])
        if i != 5:
            handle.write(", ")
    handle.close()
    # remove the image
    os.remove(
        "/Users/ue/Downloads/CXA2019/cxa2019/Product/static/images/downloaded_images/picture/trash.png"
    )
    # play the anima for each type of trash
    final_url = result_str + ".html"
    return render_template(final_url)


@app.route("/reward", methods=["GET"])
def reward():
    # TODO: trigger reward system when mistakes were spotted
    handle = open("current_user.txt", "r")
    for line in handle:
        current_user = line.strip()
    handle.close()
    con = open_DB("user.db")
    record = con.execute("SELECT Name, Points FROM User WHERE Name = \"" +
                         current_user + "\"")
    np_dict = record.fetchall()
    for line in np_dict:
        point = line["Points"]
    current_point = str(int(point) + 10)
    con.execute("UPDATE User SET Points = \"" + current_point +
                "\"WHERE Name =\"" + current_user + "\"")
    con.commit()
    # TODO: display ending page
    # return render_template("")
    return "Hey"


if __name__ == "__main__":
    app.run()