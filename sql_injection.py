from flask import Flask
from flask import request
from flask import render_template

import sqlite3
import sys
import os 

app = Flask(__name__)

@app.route("/injection",methods=['GET',"POST"])
def login():
    return render_template("index.html") 

@app.route("/xss",methods=["GET"])
def register_form():
    return render_template("register.html")

@app.route("/",methods=["POST"])
def email_manager(): 
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    
    username = request.form["username"]
    password = request.form["password"]
    
    if username and password:
        try:
            query = "SELECT email FROM users where username='{}' AND password='{}'".format(username,password)
            print(query, file=sys.stderr)
            cursor.execute(query)

            result = cursor.fetchall()
        finally:
            cursor.close()
            conn.close()
    else:
        result = "ユーザー名またはパスワードが間違っています" 

    return render_template("index.html",emails=result)
    
@app.route("/xss_confirm",methods=["POST"])
def xss_confirm():
    name = request.form["name"]
    email = request.form["email"]

    return render_template("confirm.html",name=name,email=email)

@app.route("/inquiry",methods=["GET","POST"])
def inquiry():
    result = ""
    if request.method == "POST":
        email = request.form["email"]
        inquiry = request.form["inqu"]
    
        #result = subprocess.check_output(["/usr/sbin/sendmail -i <template.txt %s"%(email)])
        result = os.system("echo %s"%(email))

        return render_template("inquiry.html",result=result)

def main():

    app.run(debug=True, host='0.0.0.0', port=8888)

if __name__ == "__main__":
    main()
    
