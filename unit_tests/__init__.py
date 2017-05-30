import os

from flask import Flask
from flask.testing import FlaskClient

from webapp.routes import api
from webapp.model import db

app = Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DB_URI', 'postgresql://localhost/devjektest')
db.init_app(app)
app.register_blueprint(api, url_prefix='')
