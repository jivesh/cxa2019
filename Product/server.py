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
#disable cacheing to force displayed picture to update
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

@app.route("/")
def root():
    return render_template("log_in.html")


@app.route("/main_page", methods=["POST"])
def main_page():
    con = open_DB('user.db')
    input_name = request.form["user_name"]
    try:
        record = con.execute("SELECT Name, Points FROM User WHERE Name = \"" +
                             input_name + "\"")
        np_dict = record.fetchall()
        if len(np_dict) == 0:
            raise ValueError 
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


# processing screen
@app.route("/process", methods=["GET"])
def process():
    return render_template("loading.html")


# triggered after shortly entering the processing screen
@app.route("/classify", methods=["GET"])
def classify():
    global image_dir
    # to make sure the image saved
    time.sleep(0.1)
    #download directory
    handle = open("DOWNLOAD DIRECTORY.txt", "r")
    for line in handle:
        download_dir = line.replace("\\","/") + "/trash.png"
    handle.close()
    #construct destination of the image
    current_dir = os.getcwd().replace("\\","/")
    image_dir = current_dir + "/static/images/downloaded_images/picture/trash.png"
    # move image from download folder to classification folder
    os.replace(download_dir, image_dir)
    # run the deep learning model and make prediction of the classification
    os.system('final_garbage.py')
    # retreive the type of trash
    result = open("prediction.txt", "r")
    for line in result:
        result_str = line
    result.close()
    open('prediction.txt', 'w').close()
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
    # play the anima for each type of trash
    final_url = result_str + ".html"
    return render_template(final_url)


@app.route("/reward", methods=["GET"])
def reward():
    # remove the image
    os.remove(image_dir)
    # update the points of the user in the database
    handle = open("current_user.txt", "r")
    for line in handle:
        current_user = line.strip()
    handle.close()
    open('current_user.txt', 'w').close()
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
    # display ending page which will lead to log_in page while showing the points
    return render_template("end.html", points=current_point)


if __name__ == "__main__":
    app.run()
