import os
import json
import decimal
import datetime
from http import HTTPStatus
from typing import Optional
from flask import Flask, request, redirect, url_for, Response
from flask_migrate import Migrate

# https://flask.palletsprojects.com/en/2.0.x/patterns/appfactories/


class CustomJsonEncoder(json.JSONEncoder):
    """ serialize common types """

    def default(self, obj):
        if isinstance(obj, decimal.Decimal):
            # Convert decimal instances to strings.
            return str(obj)
        elif isinstance(obj, datetime.datetime):
            return obj.isoformat()
        return super(CustomJsonEncoder, self).default(obj)


""" Not working
def http_redirect() -> Optional[Response]:
    print("In redirect")
    if request.scheme == 'https':
        return redirect(url_for(request.endpoint,
                                _scheme='http',
                                _external=True),
                        HTTPStatus.PERMANENT_REDIRECT)
"""


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    """
    if app.env != 'production':
        app.before_request(http_redirect)
    """
    app.secret_key = 'ShouldBeHidden!'
    app.config.from_mapping(
        SECRET_KEY='dev',
        SQLALCHEMY_DATABASE_URI='postgresql://postgres@localhost:5432/portfolio',
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
        SQLALCHEMY_ECHO=True
    )
    app.json_encoder = CustomJsonEncoder

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    from .models import db
    db.init_app(app)
    Migrate(app, db)

    from .api import users, authors, blogs, blog_entries, comments
    app.register_blueprint(users.bp)
    app.register_blueprint(authors.bp)
    app.register_blueprint(blogs.bp)
    app.register_blueprint(blog_entries.bp)
    app.register_blueprint(comments.bp)

    return app
