from flask import Blueprint, jsonify

# routes
from webapp.routes.orders import register_orders_routes

api = Blueprint('api', __name__)

register_orders_routes(api)
