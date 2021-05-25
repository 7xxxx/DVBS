from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, current_app, url_for
)

import os
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
        new_username = request.form['username']
        new_password = request.form['password']
        delete = int(request.form['delete'])
        process_request(new_username, new_password, delete)

    elif request.method == 'GET' and len(request.args) > 0:
        new_username = request.args.get("username")
        new_password = request.args.get("password")
        delete = int(request.args.get("delete"))
        process_request(new_username, new_password, delete)

    return render_template('user/profile.html', user=username)


def process_request(username, password, delete):
    user_id = session.get('user_id')
    db = get_db()
    msg = None
    error = None

    if delete == 1:
        delete_profile(user_id, db)
        msg = "profile deleted"
    elif username and password:
        error = update_username(user_id, username, db)
        if error is None:
            update_password(user_id, password, db)
            msg = "username and password updated"
    elif username:
        error = update_username(user_id, username, db)
        if error is None:
            msg = "username updated"
    elif password:
        update_password(user_id, password, db)
        msg = "password updated"

    if error:
        flash(error, 'error')
        return False
    else:
        flash(msg)
        return True


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

@bp.route('/photo', methods=('GET', 'POST'))
@login_required
def photo():
    file_path = current_app.config['FILEPATH']

    if request.method == 'POST':
        f = request.files['file']

        if f:
            i = request.form['id']
            p = os.path.join(file_path, i)
            try:
                os.makedirs(p)
            except OSError:
                pass
            print(os.path.join(p, f.filename))

            f.save(os.path.join(p, f.filename))
            flash("File: '" + os.path.join(p, f.filename) + "' saved.")
        else:
            flash("No file selected.")
    else:
        pass
    return redirect(url_for('user.profile', username="admin"))
