from flask import Flask, render_template, request, url_for, flash
from werkzeug.utils import redirect
from flask_mysqldb import MySQL
import os

app = Flask(__name__)
app.secret_key = 'many random bytes'

#  READ MYSQL SETTINGS FROM ENVIRONMENT VARIABLES
app.config['MYSQL_HOST'] = os.environ.get("shuttle.proxy.rlwy.net")
app.config['MYSQL_USER'] = os.environ.get("root")
app.config['MYSQL_PASSWORD'] = os.environ.get("FJLNdOJFEBYWAEUvuSWQIuOtxipsiBbI")
app.config['MYSQL_DB'] = os.environ.get("railway")
app.config['MYSQL_PORT'] = int(os.environ.get("37533", 3306))

mysql = MySQL(app)

@app.route('/')
def Index():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM students")
    data = cur.fetchall()
    cur.close()

    return render_template('index.html', students=data)

@app.route('/insert', methods=['POST'])
def insert():
    if request.method == "POST":
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        cur = mysql.connection.cursor()

        # Check if email or phone already exists
        cur.execute("SELECT * FROM students WHERE email=%s OR phone=%s", (email, phone))
        existing = cur.fetchone()

        if existing:
            flash("User with this email or phone already exists!")
        else:
            cur.execute("INSERT INTO students (name, email, phone) VALUES (%s, %s, %s)", (name, email, phone))
            mysql.connection.commit()
            flash("Data Inserted Successfully")

        cur.close()
        return redirect
