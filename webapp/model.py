import datetime
import pytz

from webapp.db import db


class Orders(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    organization = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    number_of_pages = db.Column(db.Integer)
    number_of_days = db.Column(db.Integer)
    status = db.Column(db.String(80))
    created_at = db.Column(db.DateTime(timezone=True), default=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC))
    updated_at = db.Column(db.DateTime(timezone=True), onupdate=datetime.datetime.utcnow().replace(tzinfo=pytz.UTC))

    def __init__(self, name, email, organization, number_of_days, number_of_pages, phone=None, status=None):
        self.name = name
        self.email = email
        self.organization = organization
        self.number_of_days = number_of_days
        self.number_of_pages = number_of_pages
        self.phone = phone
        self.status

    def as_json(self):
        return {
            "id": self.id,
            "name": self.name,
            "organization": self.organization,
            "email": self.email,
            "phone": self.phone,
            "number_of_pages": self.number_of_pages,
            "number_of_days": self.number_of_days,
            "status": self.status,
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }
