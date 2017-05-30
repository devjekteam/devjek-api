import os
from pytz import timezone
from sparkpost import SparkPost
from datetime import timedelta
from pyrfc3339 import generate

sp = SparkPost(os.environ.get('SPARKPOST_API_KEY', 'b6ba8b2e174c24093821100b6d7885f5824ca7d0'))
DEV_EMAIL = "dev@devjek.com"

def send_new_order_email(order):
    substitution_data = dict(
        name=order.name,
        organization=order.organization,
        email=order.email,
        phone=order.phone,
        number_of_days=order.number_of_days,
        number_of_pages=order.number_of_pages,
        date_created=order.created_at.__str__()
    )

    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[DEV_EMAIL],
        template="new-devjek-order-for-us",
        transactional=True,
        substitution_data=substitution_data
    )
    return response

def send_new_order_email_client(order):
    substitution_data = dict(
        name=order.name,
        organization=order.organization,
        email=order.email,
        phone=order.phone,
        number_of_days=order.number_of_days,
        number_of_pages=order.number_of_pages,
        date_created=order.created_at.__str__()
    )

    response = sp.transmissions.send(
        use_sandbox=False,
        recipients=[DEV_EMAIL],
        template="new-devjek-order-for-client",
        transactional=True,
        substitution_data=substitution_data
    )
    return response
