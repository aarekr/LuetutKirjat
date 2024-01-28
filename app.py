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
    result = db.session.execute(text("SELECT * FROM lkbookstesti"))
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
    sql = text("INSERT INTO lkbookstesti (author, title, completed) VALUES (:author, :title, :completed)")
    db.session.execute(sql, {"author":author, "title":title, "completed":completed})
    db.session.commit()
    return render_template("bookaddedtolist.html", author=author, title=title)

@app.route("/book/<int:id>")
def book_info(id):
    sql = text("SELECT * FROM lkbookstesti WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    book = result.fetchall()[0]
    return render_template("bookinfo.html", book=book)
