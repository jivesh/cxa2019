import sqlite3

con = sqlite3.connect("user.db")

try:
    con.execute("CREATE TABLE User " +
                " (Name TEXT PRIMARY KEY, Points INTEGER )")
except Exception as err:
    print(str(err))

while True:
    name = input("Enter User name: \n")
    if name == "":
        break
    points = input("Enter current points of the User:\n")
    try:
        con.execute("INSERT INTO User(Name, Points) VALUES(?, ?)",
                    (name, points))
    except Exception as err:
        print(str(err), "Try another id")
        continue
    con.commit()
con.close()
