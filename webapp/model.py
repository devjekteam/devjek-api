import datetime
import pytz

from webapp.db import db


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC))

    def __init__(self):
        pass
