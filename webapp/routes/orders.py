from flask import request, jsonify
from flask.views import MethodView

# local
from .decorators import required_params
from webapp.model import db, Orders
from webapp.integrations.sparkpost import send_new_order_email


def register_orders_routes(blueprint):
    view_func = OrdersRoutes.as_view('orders')
    blueprint.add_url_rule('/orders/<int:order_id>', strict_slashes=False, view_func=view_func, methods=['GET', 'PUT'])
    blueprint.add_url_rule('/orders', strict_slashes=False, view_func=view_func, methods=['GET', 'POST'])

class OrdersRoutes(MethodView):

    def get(self, order_id=None):
        if not order_id:
            all_orders = Orders.query.all()
            return jsonify(orders=[o.as_json() for o in all_orders]), 200

        order = Orders.query.filter_by(id=order_id).first()
        if not order:
            return jsonify(error="Order with id %d does not exist" % order_id), 400

        return jsonify(order.as_json()), 200

    @required_params("name", "email", "organization", "number_of_pages", "number_of_days")
    def post(self):
        """
        Create new order
        @params
        - name (required): <string>
        - email (required): <string>
        - organization (required): <string>
        - number_of_pages (required): <int> requested number of pages to convert
        - number_of_days (required): <int> requested number of days for deliverables
        - phone: <string>
        - status: <string>
        """
        params = request.json

        kwargs = {
            "name": params.get("name"),
            "email": params.get("email"),
            "organization": params.get("organization"),
            "number_of_pages": params.get("number_of_pages"),
            "number_of_days": params.get("number_of_days"),
            "phone": params.get("phone"),
            "status": params.get("status"),
        }

        order = Orders(**kwargs)

        db.session.add(order)
        db.session.commit()

        # send us an email about new order
        send_new_order_email(order)

        return jsonify(order.as_json()), 201

    def put(self, order_id):
        params = request.json

        order = Orders.query.filter_by(id=order_id).first()
        if not order:
            return jsonify(error="Order with id %d does not exist" % order_id), 400

        for key, value in params.items():
            if hasattr(order, key):
                setattr(order, key, value)

        db.session.add(order)
        db.session.commit()

        return jsonify(order.as_json()), 200
