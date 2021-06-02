from flask import (
    Blueprint, flash, g, redirect, render_template, request, session,
    current_app, url_for
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
    db = get_db()
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

    user = db.execute("SELECT * from user WHERE username = ?", (username,)).fetchone()

    return render_template('user/profile.html', user=username, img=user['image'])


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
    db = get_db()
    img_path = current_app.config['IMGPATH']

    if request.method == 'POST':
        f = request.files['file']

        if f:
            i = request.form['id']

            fpath = os.path.join(img_path, i) # e.g. images/1
            sloc = os.path.join(current_app.static_folder, fpath) # e.g xyz/app/static/images/1

            try:
                os.makedirs(sloc)
            except OSError:
                pass

            fpath = os.path.join(fpath, f.filename)
            sloc = os.path.join(sloc, f.filename)

            f.save(sloc)
            db.execute("UPDATE user SET image = ? WHERE id = ?", (fpath, i,))
            db.commit()
            flash("File: '" + fpath + "' saved.")
        else:
            flash("No file selected.")
    else:
        pass
    return redirect(url_for('user.profile', username="admin"))
