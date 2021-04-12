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
    statement = 'SELECT * FROM book WHERE request = 1'
    requests = db.execute(statement)

    return render_template('book/inquiry.html', requests=requests)
