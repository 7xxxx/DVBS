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
from werkzeug.utils import secure_filename
import filetype
from copy import copy

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

def allowed_file(filename):
    """
    Check that the given file is a jpg
    or png.
    """
    kind = filetype.guess(filename)
    filename.seek(0) # restore file pointer
    return kind and kind.mime in ['image/png', 'image/jpg']


@bp.route('/photo/<uid>', methods=('GET', 'POST'))
@login_required
def photo(uid):
    db = get_db()
    img_path = current_app.config['IMGPATH']
    user_id = session.get('user_id')
    
    if request.method == 'POST':
        f = request.files['file']
        
        if f and allowed_file(f) and int(uid) == int(user_id):
            # Storage location, e.g xyz/app/static/images,
            # isnt controlled by the user anymore.
            sloc = os.path.join(current_app.static_folder, img_path)

            try:
                os.makedirs(sloc)
            except OSError:
                pass
            
            # Normalize file name
            fname = secure_filename(f.filename)
            
            # File path for user
            fpath = os.path.join(img_path, fname)

            # Exact storage location
            sloc = os.path.join(sloc, fname)

            # Delet old file
            user = db.execute("SELECT * from user WHERE id = ?", (uid,)).fetchone()
            try:
                os.remove(os.path.join(current_app.static_folder, user['image']))
            except OSError:
                pass
            
            # Save file, e.g. static/images/xyz.png
            f.save(sloc)
            
            # Update file path
            db.execute("UPDATE user SET image = ? WHERE id = ?", (fpath, uid,))
            db.commit()
            flash("File: '" + fpath + "' saved.")
        else:
            flash("No file selected.")
    else:
        pass
    return redirect(url_for('user.profile', username="admin"))
