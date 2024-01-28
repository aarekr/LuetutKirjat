from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text
from os import getenv

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = getenv("DATABASE_URL")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db = SQLAlchemy(app)

all_books_list = {}
all_books_list[1] = {"author": "Juhani Aho", "title": "Rautatie", "completed": True}
all_books_list[2] = {"author": "Mika Ruohonen", "title": "Tietoturva", "completed": False}
book_id = 3

@app.route("/")
def index():
    result = db.session.execute(text("SELECT * FROM lkbookstesti"))
    db_books = result.fetchall()
    return render_template("index.html", book_list=all_books_list, db_books=db_books)

@app.route("/addbook")
def add_book():
    return render_template("formaddbook.html")

@app.route("/bookadded", methods=["POST"])
def book_added():
    global book_id
    author = request.form["author"]
    title = request.form["title"]
    print("author:", author)
    print("title :", title)
    address = "/book" + str(book_id)
    all_books_list[book_id] = {"author": author, "title": title, "completed": False}
    book_id += 1
    return render_template("bookaddedtolist.html", author=author, title=title)

@app.route("/book/<int:id>")
def book_info(id):
    book = all_books_list[int(id)]
    return render_template("bookinfo.html", book=book)
