from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

@app.route("/")
def index():
    result = db.session.execute(text("SELECT * FROM lkbooks"))
    db_books = result.fetchall()
    return render_template("index.html", db_books=db_books)

@app.route("/addbook")
def add_book():
    return render_template("formaddbook.html")

@app.route("/bookadded", methods=["POST"])
def book_added():
    author = request.form["author"]
    title = request.form["title"]
    completed = False
    sql = text("INSERT INTO lkbooks (author, title, completed) VALUES (:author, :title, :completed)")
    db.session.execute(sql, {"author":author, "title":title, "completed":completed})
    db.session.commit()
    return render_template("bookaddedtolist.html", author=author, title=title)

@app.route("/book/<int:book_id>")
def book_info(book_id):
    sql = text("SELECT * FROM lkbooks WHERE id=:id")
    result = db.session.execute(sql, {"id":book_id})
    book = result.fetchall()[0]
    return render_template("bookinfo.html", book=book)

@app.route("/bookcompleted", methods=["POST"])
def book_completed():
    id = 2
    print("book_completed funktio, book_id:", id)
    completed = True
    sql = text("UPDATE lkbooks SET completed=True WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return render_template("bookcompleted.html")
