import os

from flask import Flask, request
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from webapp.routes import api
from webapp.db import db

migrate = Migrate()

def create_app(DB_URI=None):
    application = Flask(__name__)

    # DB Connection Information
    if not DB_URI:
        DB_URI = os.environ.get('DB_URI', 'postgresql://localhost/devjekdev')

    application.config['SQLALCHEMY_DATABASE_URI'] = DB_URI
    application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # send CORS headers for frontend
    @application.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        if request.method == 'OPTIONS':
            response.headers['Access-Control-Allow-Methods'] = 'DELETE, GET, POST, PUT'
            headers = request.headers.get('Access-Control-Request-Headers')
            if headers:
                response.headers['Access-Control-Allow-Headers'] = headers
        return response

    # initialize db. any external calls to db must use application context
    db.init_app(application)
    # set up migration support for alembic
    migrate.init_app(application, db)

    # Register route blueprints
    application.register_blueprint(api)

    return application
