from flask import (
    Blueprint, flash, g, redirect, render_template, request
)
from app.auth import (
    login_required, username_exists
)

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/<username>', methods=('GET', 'POST'))
@login_required
def profile(username):
    if request.method == 'POST':
        pass

    return render_template('user/profile.html', user=username)

