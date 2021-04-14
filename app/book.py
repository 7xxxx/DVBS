import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.db import get_db

bp = Blueprint('book', __name__, url_prefix='/')


@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    statement = 'SELECT * FROM book WHERE request = 0'

    if request.method == 'POST':
        find = request.form['find']
        statement = 'SELECT * from book WHERE title LIKE "%{}%" AND request = 0'.format(find)
        print(statement)

    books = db.execute(
        statement
    )
    return render_template('book/index.html', books=books)


@bp.route('/inquiry', methods=('GET', 'POST'))
def inquiry():
    db = get_db()
    get_books = 'SELECT * FROM book WHERE request = 1'
    get_comments = 'SELECT * FROM comments'
    requests = db.execute(get_books)
    comments = db.execute(get_comments)

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

@bp.route('/comment/<id>', methods=['POST'])
def comment(bid):
    db = get_db()
    text = request.form['text']

    db.execute(
        "INSERT INTO comments (text, book_id) VALUES (?, ?)", (text, bid,)
    )
    db.commit()

    
