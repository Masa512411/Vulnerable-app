from flask import Flask
from flask import request
from flask import render_template

import sqlite3

app = Flask(__name__)

@app.route("/injection",methods=['GET',"POST"])
def login():
    return render_template("index.html") 

@app.route("/email_manager",methods=["POST"])
def email_manager(): 
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    username = str(request.form["username"])
    password = str(request.form["password"])
    try:
        query = "SELECT email FROM users where username={} AND password={}".format(username,password)
        cursor.execute(query)

        result = cursor.fetchall()
    finally:
        cursor.close()
        conn.close()

    return render_template("index.html",email=result)
    

def init_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    try:
        cursor.execute("DROP TABLE IF EXISTS users")
        cursor.execute("CREATE TABLE users (username TEXT, password TEXT, email text)")

        cursor.execute('INSERT INTO users VALUES (?,?,?)', ('Alice', "ali","alice@gmail.com"))
        cursor.execute('INSERT INTO users VALUES (?,?,?)', ('Iris', "iri","iris@gmail.com"))
        cursor.execute('INSERT INTO users VALUES (?,?,?)', ('Bob', "bob","bob@gmail.com"))

    finally:
        cursor.close()
        conn.close()

def main():
   # init_db()

    app.run(debug=True, host='0.0.0.0', port=8888)

if __name__ == "__main__":
    main()
    
