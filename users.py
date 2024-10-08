''' Module for handling user '''

from flask import session
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from db import db

def register(username, password):
    ''' New user registration '''
    hash_value = generate_password_hash(password)
    try:
        sql = text("INSERT INTO lkusers (username, password) VALUES (:username, :password)")
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except: # pylint: disable=bare-except
        return False
    return login(username, password)

def check_username_and_passwords(username, password_1, password_2):
    ''' Checking that username and passwords are valid '''
    if len(username) > 10 or len(username) < 3:
        return "Käyttäjätunnuksen on oltava 3-10 merkin pituinen"
    if len(password_1) > 20 or len(password_1) < 3:
        return "Salasanan on oltava 3-20 merkin pituinen"
    if password_1 != password_2:
        return "Salasanat eroavat"
    return "Credentials OK"

def login(username, password):
    ''' User login '''
    sql = text("SELECT id, password FROM lkusers WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    if check_password_hash(user.password, password):
        session["user_id"] = user.id
        session["username"] = username
        return True
    return False

def user_id():
    ''' User session id '''
    return session.get("user_id", 0)

def user_name(id):
    ''' User name by id '''
    sql = text("SELECT id, username FROM lkusers WHERE id=:id")
    result = db.session.execute(sql, {"id":id})
    user = result.fetchone()
    return user[1]

def logout():
    ''' User logout '''
    del session["username"]
    del session["user_id"]
