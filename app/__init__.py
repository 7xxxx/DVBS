import os

from flask import Flask
from . import db, book, auth, user


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'insecure.sqlite'),
    )

    app.config.from_pyfile('config.py', silent=True)

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






