from flask import (
    Blueprint, flash, g, redirect, render_template, request, session
)

import app.auth
from app.auth import (
    login_required, username_exists
)
from app.db import get_db
from werkzeug.security import check_password_hash, generate_password_hash

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<username>', methods=('GET', 'POST'))
@login_required
def profile(username):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        delete = int(request.form['delete'])
        user_id = session.get('user_id')
        db = get_db()
        error = None
        msg = None

        if delete == 1:
            delete_profile(user_id, db)
            msg = "profile deleted"
        elif username and password:
            error = update_username(user_id, username, db)
            update_password(user_id, password, db)
            msg = "username and password updated"
        elif username:
            error = update_username(user_id, username, db)
            msg = "username updated"
        elif password:
            update_password(user_id, password, db)
            msg = "password updated"

        if error:
            flash(error)
        else:
            flash(msg)
    return render_template('user/profile.html', user=username)


def delete_profile(user_id, db):
    db.execute("DELETE FROM user WHERE id = ?", (user_id,))
    db.commit()


def update_username(user_id, username, db):
    error = None
    if app.auth.username_exists(username, db):
        error = "Username already exists"
    else:
        db.execute("UPDATE user SET username = ? WHERE id = ?", (username, user_id,))
        db.commit()
    return error


def update_password(user_id, password, db):
    db.execute("UPDATE user SET password = ? WHERE id = ?",
               (generate_password_hash(password, method='plain', salt_length=0),
                user_id,))
    db.commit()
