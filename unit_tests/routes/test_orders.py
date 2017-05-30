import unittest
import json

from mock import patch, Mock

from unit_tests import app
from webapp.model import Orders, db


class OrdersTests(unittest.TestCase):
    def setUp(self):
        with app.app_context():
            # create client to send requests through
            self.client = app.test_client()
            # create all tables
            db.create_all()

    def tearDown(self):
        with app.app_context():
            # drop all tables
            db.drop_all()

    def test_get_all_orders(self):
        with app.app_context():
            kwargs = dict(
                name="test man dude",
                organization="E-Corp",
                email="testmandude@ecorp.com",
                phone="+18888888888",
                number_of_days=1,
                number_of_pages=10
            )
            test_order = Orders(**kwargs)
            db.session.add(test_order)
            db.session.commit()

            result = self.client.get('/orders')
            result_dict = json.loads(result.data.decode('utf-8'))

            self.assertEqual(len(result_dict["orders"]), 1)
            result_dict = result_dict["orders"][0]
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result_dict['name'], test_order.name)
            self.assertEqual(result_dict['organization'], test_order.organization)
            self.assertEqual(result_dict['email'], test_order.email)
            self.assertEqual(result_dict['phone'], test_order.phone)
            self.assertEqual(result_dict['number_of_days'], test_order.number_of_days)
            self.assertEqual(result_dict['number_of_pages'], test_order.number_of_pages)

    def test_get_order_by_id(self):
        with app.app_context():
            kwargs = dict(
                name="test man dude",
                organization="E-Corp",
                email="testmandude@ecorp.com",
                phone="+18888888888",
                number_of_days=1,
                number_of_pages=10
            )
            test_order = Orders(**kwargs)
            db.session.add(test_order)
            db.session.commit()

            result = self.client.get('/orders/%d' % test_order.id)
            result_dict = json.loads(result.data.decode('utf-8'))

            self.assertEqual(result.status_code, 200)
            self.assertEqual(result_dict['name'], test_order.name)
            self.assertEqual(result_dict['organization'], test_order.organization)
            self.assertEqual(result_dict['email'], test_order.email)
            self.assertEqual(result_dict['phone'], test_order.phone)
            self.assertEqual(result_dict['number_of_days'], test_order.number_of_days)
            self.assertEqual(result_dict['number_of_pages'], test_order.number_of_pages)

    def test_get_plan_bad_id(self):
        with app.app_context():
            result = self.client.get('/orders/2')

            self.assertEqual(result.status_code, 400)

    @patch('webapp.routes.orders.send_new_order_email', return_value=True)
    def test_post_create_new_order(self, mock_sparkpost):
        with app.app_context():
            json_payload = dict(
                name="test man dude",
                organization="E-Corp",
                email="testmandude@ecorp.com",
                phone="+18888888888",
                number_of_days=1,
                number_of_pages=10
            )

            result = self.client.post('/orders/', data=json.dumps(json_payload),
                                  content_type='application/json')

            result_dict = json.loads(result.data.decode('utf-8'))
            self.assertEqual(result.status_code, 201)
            self.assertEqual(result_dict['name'], json_payload["name"])
            self.assertEqual(result_dict['organization'], json_payload["organization"])
            self.assertEqual(result_dict['email'], json_payload["email"])
            self.assertEqual(result_dict['phone'], json_payload["phone"])
            self.assertEqual(result_dict['number_of_days'], json_payload["number_of_days"])
            self.assertEqual(result_dict['number_of_pages'], json_payload["number_of_pages"])

    @patch('webapp.routes.orders.send_new_order_email', return_value={})
    def test_post_create_new_order_bad_params(self, mock_sparkpost):
        with app.app_context():
            json_payload = {
                "not-name": "test"
            }

            result = self.client.post('/orders/', data=json.dumps(json_payload),
                                  content_type='application/json')

            result_dict = json.loads(result.data.decode('utf-8'))
            self.assertEqual(result.status_code, 400)

    def test_put_edit_user(self):
        with app.app_context():
            order1_kwargs = dict(
                name="test man dude",
                organization="E-Corp",
                email="testmandude@ecorp.com",
                phone="+18888888888",
                number_of_days=1,
                number_of_pages=10
            )

            order1 = Orders(**order1_kwargs)
            db.session.add(order1)
            db.session.commit()


            json_payload = dict(
                name = 'changed',
                email = 'changed',
                number_of_days = 7)

            result = self.client.put('/orders/%d' % order1.id, data=json.dumps(json_payload),
                                  content_type='application/json')

            result_dict = json.loads(result.data.decode('utf-8'))
            self.assertEqual(result.status_code, 200)
            self.assertEqual(result_dict['name'], json_payload["name"])
            self.assertEqual(result_dict['email'], json_payload["email"])
            self.assertEqual(result_dict['number_of_days'], json_payload["number_of_days"])

    def test_put_edit_user_no_matching_params(self):
        with app.app_context():
            order1_kwargs = dict(
                name="test man dude",
                organization="E-Corp",
                email="testmandude@ecorp.com",
                phone="+18888888888",
                number_of_days=1,
                number_of_pages=10
            )

            order1 = Orders(**order1_kwargs)
            db.session.add(order1)
            db.session.commit()

            json_payload = {'param_not_included': 'changed'}

            result = self.client.put('/orders/%d' % order1.id, data=json.dumps(json_payload),
                                  content_type='application/json')

            result_dict = json.loads(result.data.decode('utf-8'))
            self.assertEqual(result.status_code, 200)
            self.assertNotIn('param_not_included', result_dict)
