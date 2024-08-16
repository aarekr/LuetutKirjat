''' Routes for the app '''

from flask import render_template, request, redirect, session
from sqlalchemy.sql import text

from app import app
from db import db
import users

@app.route("/")
def index():
    ''' Front page and all books '''
    current_user = users.user_id()
    result = db.session.execute(text("SELECT * FROM lkbooks WHERE user_id=" + str(current_user)))
    db_books = result.fetchall()
    return render_template("index.html", db_books=db_books)

# register, login, logout
@app.route("/register", methods=["GET", "POST"])
def register():
    ''' New user registration '''
    if request.method == "GET":
        return render_template("register.html")
    if request.method == "POST":
        username = request.form["username"]
        password_1 = request.form["password_1"]
        password_2 = request.form["password_2"]
        if len(username) > 10:
            return render_template("error.html", return_to_page="registration",
                                   message="Käyttäjätunnuksen maksimipituus on 10 merkkiä")
        if len(password_1) > 20:
            return render_template("error.html", return_to_page="registration",
                                   message="Salasanan maksimipituus on 20 merkkiä")
        if password_1 != password_2:
            return render_template("error.html", return_to_page="registration",
                                   message="Salasanat eroavat")
        if users.register(username, password_1):
            return redirect("/")
        else:
            return render_template("error.html", return_to_page="registration",
                                   message="Rekisteröinti ei onnistunut")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    ''' User login '''
    if request.method == "GET":
        return render_template("login.html")
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("error.html", message="Väärä tunnus tai salasana")

@app.route("/logout")
def logout():
    ''' User logout from the application '''
    del session["username"]
    del session["user_id"]
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
    user_id = users.user_id()
    if user_id == 0:
        return False
    title = request.form["title"]
    author = request.form["author"]
    reading_started = False
    reading_completed = False
    book_language = request.form["book_language"]
    stars = 0
    visible = True
    sql = text("INSERT INTO lkbooks (title, author, reading_started, reading_completed, \
               book_language, stars, visible, user_id) VALUES (:title, :author, :reading_started, \
               :reading_completed, :book_language, :stars, :visible, :user_id)")
    db.session.execute(sql, {"title":title, "author":author, "reading_started":reading_started, \
                             "reading_completed":reading_completed, \
                             "book_language":book_language, "stars":stars, "visible":visible, \
                             "user_id":user_id})
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
    # the book should be removed from the readers list
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

# statistics: overview of what all users have read
@app.route("/statistics")
def get_stats():
    ''' Showing statistics of read books by all users '''
    result_books = db.session.execute(text("SELECT * FROM lkbooks"))
    db_books = result_books.fetchall()
    result_users = db.session.execute(text("SELECT id, username FROM lkusers"))
    book_dict = {}
    for book in db_books:
        if book.title not in book_dict:
            book_dict[book.title] = {"id": [], "readers": "", "readers_count": 0}
        book_dict[book.title]["id"].append(book.user_id)
        if len(book_dict[book.title]["readers"]) == 0:
            book_dict[book.title]["readers"] += users.user_name(book.user_id)
        else:
            book_dict[book.title]["readers"] += ", " + users.user_name(book.user_id)
        book_dict[book.title]["author"] = book.author
        book_dict[book.title]["readers_count"] += 1
    db_users = result_users.fetchall()
    current_user = users.user_id()
    return render_template("statistics.html", db_books=db_books, book_dict=book_dict,
                           db_users=db_users, current_user=current_user)
