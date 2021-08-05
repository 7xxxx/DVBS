import sqlite3
import time

import markdown
from flask import (
    Blueprint, redirect, render_template, request, url_for
)

from app.db import get_db

bp = Blueprint('book', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    statement = 'SELECT * FROM book WHERE request = 0'

    db.create_function("sleep", 1, time.sleep)

    if request.method == 'POST':
        find = request.form['find']
        statement = 'SELECT * from book WHERE title LIKE "%{}%" AND request = 0'.format(find)
        print(statement)

    try:
        books = db.execute(
            statement
        ).fetchall()
    except sqlite3.OperationalError as err:
        return render_template('book/index.html', error=err)

    comments = get_comments()
    return render_template('book/index.html', books=books, comments=comments)


@bp.route('/inquiry', methods=('GET', 'POST'))
def inquiry():
    db = get_db()
    get_books = 'SELECT * FROM book WHERE request = 1'
    requests = db.execute(get_books).fetchall()
    comments = get_comments() 

    if request.method == 'POST':
        isbn = request.form['isbn']
        title = request.form['title']
        author = request.form['author']
        publisher = request.form['publisher']

        db.execute(
            "INSERT INTO book (isbn, title, author, publisher, request) VALUES (?, ?, ?, ?, 1)", (isbn, title, author, publisher,)
        )
        db.commit()

    return render_template('book/inquiry.html', requests=requests, comments=comments)


@bp.route('/comment/<bid>', methods=['POST'])
def comment(bid):
    db = get_db()
    text = request.form['text']

    db.execute(
        "INSERT INTO comments (text, book_id) VALUES (?, ?)", (text, bid,)
    )
    db.commit()
    
    if request.environ['HTTP_ORIGIN'] is not None:
        return redirect(request.environ['HTTP_ORIGIN'])
    else:
        return redirect(url_for('book.index'))

def get_comments():
    """
    Select all comments from the database and
    transform their md syntax into valid html.
    """
    db = get_db()
    comments = db.execute("SELECT * FROM comments").fetchall()
    parsed_comments = []

    for comment in comments:
        l = list(comment)
        parsed_comments.append(
                {
                    "id" : l[0],
                    "text" : markdown.markdown(l[1]),
                    "book_id" : l[2],
                }
        )
        
    return parsed_comments


    
