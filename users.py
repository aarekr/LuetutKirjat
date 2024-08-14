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
    except:
        return False
    return login(username, password)

def login(username, password):
    ''' User login '''
    sql = text("SELECT id, password FROM lkusers WHERE username=:username")
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        if check_password_hash(user.password, password):
            session["user_id"] = user.id
            session["username"] = username
            return True
        else:
            return False

def user_id():
    ''' User session id '''
    return session.get("user_id", 0)

def logout():
    ''' User logout '''
    del session["username"]
    del session["user_id"]
