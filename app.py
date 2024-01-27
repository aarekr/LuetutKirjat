from flask import Flask, render_template, request

app = Flask(__name__)

all_books_list = {}
all_books_list[1] = {"author": "Juhani Aho", "title": "Rautatie", "completed": True}
all_books_list[2] = {"author": "Mika Ruohonen", "title": "Tietoturva", "completed": False}
book_id = 3

@app.route("/")
def index():
    return render_template("index.html", book_list=all_books_list)

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
    all_books_list[book_id] = {"author": author, "title": title, "completed": False}
    book_id += 1
    return render_template("bookaddedtolist.html", author=author, title=title)
