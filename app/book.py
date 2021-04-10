import functools

from flask import(
    Blueprint, flash, g, redirect, render_template, request, url_for
)

from app.db import get_db

bp = Blueprint('book', __name__, url_prefix='/')

@bp.route('/', methods=('GET', 'POST'))
def index():
    db = get_db()
    statement = 'SELECT * FROM book'

    if request.method == 'POST':
        find = request.form['find']
        statement = 'SELECT * from book WHERE title LIKE "%{}%"'.format(find)
        print(statement)

    books = db.execute(
       statement
    )
    return render_template('index.html', books=books)

# %" union select *, Null as Col4, Null as Col5 from user--
