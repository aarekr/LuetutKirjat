''' Routes for the app '''

from flask import render_template, request, redirect, session
from sqlalchemy.sql import text

#from werkzeug.security import check_password_hash, generate_password_hash
from app import app
from db import db
import users

@app.route("/")
def index():
    ''' Front page and all books '''
    result = db.session.execute(text("SELECT * FROM lkbooks"))
    db_books = result.fetchall()
    return render_template("index.html", db_books=db_books)

# register, login, logout
@app.route("/register", methods=["GET", "POST"])
def register():
    ''' New user registration '''
    print("routes register")
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password_1 = request.form["password_1"]
        password_2 = request.form["password_2"]
        print("routes POST: ", username, password_1)
        if password_1 != password_2:
            return render_template("error.html", message="Salasanat eroavat")
        if users.register(username, password_1):
            return redirect("/")
        return render_template("error.html", message="Rekisteröinti ei onnistunut")

@app.route("/login", methods=["GET", "POST"])
def login():
    ''' User login '''
    username = request.form["username"]
    password = request.form["password"]
    # check username and password
    print("routes login: ", username, password)
    session["username"] = username
    #return redirect("/")
    print("routes login request.method: ", request.method)
    if request.method == "GET":
        return render_template("login.html")
    '''if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        print("routes login: ", username, password)
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")'''
    return redirect("/")

@app.route("/logout")
def logout():
    ''' User logout from the application '''
    del session["username"]
    return redirect("/")


# form for adding a new book to the reading list
@app.route("/addbook")
def add_book():
    ''' Form for adding a new book to the reading list '''
    return render_template("formaddbook.html")

# adding a new book to the reading list and confirming it
@app.route("/bookadded", methods=["POST"])
def book_added():
    ''' Adding a book to the reading list '''
    title = request.form["title"]
    author = request.form["author"]
    reading_started = False
    reading_completed = False
    book_language = request.form["book_language"]
    stars = 0
    visible = True
    sql = text("INSERT INTO lkbooks (title, author, reading_started, reading_completed, \
               book_language, stars, visible) VALUES (:title, :author, :reading_started, \
               :reading_completed, :book_language, :stars, :visible)")
    db.session.execute(sql, {"title":title, "author":author, "reading_started":reading_started, \
                             "reading_completed":reading_completed, \
                             "book_language":book_language, "stars":stars, "visible":visible})
    db.session.commit()
    return render_template("bookaddedtolist.html", title=title, author=author)

# book info page displaying details
@app.route("/bookinfo/<int:id>")
def book_info(id):
    ''' Displaying book info '''
    sql = text("SELECT * FROM lkbooks WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    book = result.fetchall()[0]
    return render_template("bookinfo.html", book=book)

@app.route("/givestars/<int:id>", methods=["POST"])
def give_stars(id):
    ''' Rating a book with 1-5 stars '''
    try:
        stars = request.form["stars"]
        sql = text("UPDATE lkbooks SET stars=:stars WHERE id=:id")
        db.session.execute(sql, {"id":id, "stars":stars})
        db.session.commit()
        return redirect("/")
    except:
        address = "/bookinfo/" + str(id) + "?id=" + str(id)
        # add notification here
        return redirect(address)

# mark book as reading started
@app.route("/bookstarted/<int:id>", methods=["POST"])
def book_started(id):
    ''' Marking a book as reading started '''
    sql = text("UPDATE lkbooks SET reading_started=True WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/")

# mark book as reading completed
@app.route("/bookcompleted/<int:id>", methods=["POST"])
def book_completed(id):
    ''' Marking a book as reading completed '''
    sql = text("UPDATE lkbooks SET reading_started=False, reading_completed=True WHERE id=:id")
    db.session.execute(sql, {"id":id})
    db.session.commit()
    return redirect("/")

# removing/hiding a book from the list
@app.route("/removebook/<int:id>", methods=["POST"])
def remove_book(id):
    ''' Deleting/hiding books from the read books list '''
    visible = False
    sql = text("UPDATE lkbooks SET visible=:visible WHERE id=:id")
    db.session.execute(sql, {"id":id, "visible":visible})
    db.session.commit()
    return redirect("/")

# search book main page
@app.route("/searchbook")
def search_book():
    ''' Main page of search books functionality '''
    return render_template("searchbookmainpage.html")

# searhing a book by author name
@app.route("/searchauthor")
def search_author():
    ''' Searching books by author '''
    query = request.args["query"]
    # handle uppercase and lowercase
    sql = text("SELECT title, author, reading_started, reading_completed, book_language, stars \
                FROM lkbooks WHERE author LIKE :query")
    result = db.session.execute(sql, {"query":"%"+query+"%"})
    searched_books = result.fetchall()
    count=len(searched_books)
    return render_template("searchedbooks.html", searched_books=searched_books, count=count)
