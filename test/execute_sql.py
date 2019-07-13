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

con = open_DB('user.db')
# input_name = request.form["name"]
input_name="JV"
point = -1
try:
    # print("sabhdkjgfevhjkawegf")
    record = con.execute("SELECT Name, Points FROM User WHERE Name = \"" + input_name + "\"")
    np_dict = record.fetchall()
    # print("sabhdkjgfevhjkawegf")
    for line in np_dict:
        point = line["Points"]
        # print("sabhdkjgfevhjkawegf")
except Exception as e:
    print("hi")
    print(str(e))
    point = 0
    con.execute("INSERT INTO User (Name, Points) VALUES(?, ?)",
                (input_name, point))
    con.commit()
print("points", point)