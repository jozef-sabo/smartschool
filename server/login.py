from passlib.hash import bcrypt
import mysql.connector

# SECRETS IMPORT
DATABASE_HOST = ""
DATABASE_PORT = 0
DATABASE_NAME = ""
DATABASE_USER = ""
DATABASE_PASSWORD = ""
try:
    from secrets import *
except ImportError:
    pass


def login(form):
    mariadb_connect = mysql.connector.connect(user=DATABASE_USER, password=DATABASE_PASSWORD, database=DATABASE_NAME,
                                              port=DATABASE_PORT, host=DATABASE_HOST)
    user_name = form['username']
    password = form['password']
    cur = mariadb_connect.cursor(buffered=True)
    cur.execute("SELECT `password` FROM users WHERE username='%s'" % user_name)

    data = cur.fetchall()
    cur.close()
    mariadb_connect.close()

    if len(data) != 1:
        return False

    pwd_database = data[0][0].decode()

    return bcrypt.verify(password, pwd_database)


"""
    if sha256_crypt.verify(password, data):
        account = True

    if account:
        session['logged_in'] = True
    else:
        flash('wrong password!')
    return home()

from flask import Flask
from flask import Flask, flash, redirect, render_template, request, session, abort

import os
import operator
app = Flask(__name__)
mariadb_connect = mariadb.connect(user='chooseAUserName', password='chooseAPassword', databse='Login')
@app.route('/')
def home():
  if not session.get('logged_in'):
    return render_template('login.html')
  else:
    return render_template('index.html')


@app.route('logout')
def logout():
  session['logged_in'] = False
  return home()

if __name__ == "__main__":
  app.secret_key = os.urandom(12)
  app.run(debug=False,host='0.0.0.0', port=5000)
"""

login({"username": "Vrabel", "password": "ferinoaa"})
