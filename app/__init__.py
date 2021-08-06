import os

from flask import Flask
from . import db, book, auth, user
from flask_talisman import Talisman

csp = {
    'default-src': [
        '\'self\'',
        'https://cdn.jsdelivr.net'
    ],
    'img-src': [
        '\'self\'',
        'https://picsum.photos',
        '*.picsum.photos',
        'https://bulma.io'
    ]
}


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    Talisman(app, content_security_policy=csp)
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY') or 'abc',
        DATABASE=os.path.join(app.instance_path, 'insecure.sqlite'),
        IMGPATH="images",
        MAX_CONTENT_LENGTH=5 * 1024 * 1024,
        SESSION_COKIE_SECURE=True,
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax'
    )

    app.config.from_pyfile('config.py', silent=True)

    # Create required directories if they don't exist
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass
    
    # Initialize database
    db.init_app(app)

    # register book blueprint
    app.register_blueprint(book.bp)

    # register auth blueprint
    app.register_blueprint(auth.bp)

    # register profile blueprint
    app.register_blueprint(user.bp)

    return app






