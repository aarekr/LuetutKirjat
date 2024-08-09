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
    title = request.form["title"]
    author = request.form["author"]
    reading_started = False
    reading_completed = False
    book_language = request.form["book_language"]
    stars = 0
    sql = text("INSERT INTO lkbooks (title, author, reading_started, reading_completed, book_language, stars) \
               VALUES (:title, :author, :reading_started, :reading_completed, :book_language, :stars)")
    db.session.execute(sql, {"title":title, "author":author, "reading_started":reading_started, \
                             "reading_completed":reading_completed, "book_language":book_language, "stars":stars})
    db.session.commit()
    return render_template("bookaddedtolist.html", title=title, author=author)

# book info page displaying details
@app.route("/bookinfo/<int:id>")
def book_info(id):
    sql = text("SELECT * FROM lkbooks WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    book = result.fetchall()[0]
    return render_template("bookinfo.html", book=book)

# mark book as reading started
@app.route("/bookstarted/<int:id>", methods=["POST"])
def book_started(id):
    sql = text("UPDATE lkbooks SET reading_started=True WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/")

# mark book as reading completed
@app.route("/bookcompleted/<int:id>", methods=["POST"])
def book_completed(id):
    sql = text("UPDATE lkbooks SET reading_started=False, reading_completed=True WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/")
