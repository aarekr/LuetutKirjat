from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv
from werkzeug.security import check_password_hash, generate_password_hash

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.secret_key = getenv("SECRET_KEY")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT * FROM lkbooks"))
    db_books = result.fetchall()
    return render_template("index.html", db_books=db_books)

@app.route("/login",methods=["POST"])
def login():
    username = request.form["username"]
    password = request.form["password"]
    # TODO: check username and password
    session["username"] = username
    return redirect("/")

@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")

# form for adding a new book to the reading list
@app.route("/addbook")
def add_book():
    return render_template("formaddbook.html")

# adding a new book to the reading list and confirming it
@app.route("/bookadded", methods=["POST"])
def book_added():
    author = request.form["author"]
    title = request.form["title"]
    completed = False
    sql = text("INSERT INTO lkbooks (author, title, completed) VALUES (:author, :title, :completed)")
    db.session.execute(sql, {"author":author, "title":title, "completed":completed})
    db.session.commit()
    return render_template("bookaddedtolist.html", author=author, title=title)

# book info page displaying details
@app.route("/book/<int:id>")
def book_info(id):
    sql = text("SELECT * FROM lkbooks WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    book = result.fetchall()[0]
    return render_template("bookinfo.html", book=book)

@app.route("/bookcompleted/<int:id>", methods=["POST"])
def book_completed(id):
    #book_id = request.form["id"]
    sql = text("UPDATE lkbooks SET completed=True WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return render_template("index.html")
