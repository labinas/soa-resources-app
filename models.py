import re
import resource
from app import db
from enum import Enum

class ResourceType(Enum):
    ROOM = 1
    FOOD = 2
    TOYS = 3
    MEDICATION = 4

#id, name, resourcetype
class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    type = db.Column(Enum(ResourceType))

    def __init__(self, name, type):
        self.name = name
        self.type = type


class BookResource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    resource_id = db.Column(db.Integer, db.ForeignKey('resource.id'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)


    def __init__(self, resource_id, quantity):
        self.resource_id = resource_id
        self.quantity = quantity


class Appointment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_from = db.Column(db.DateTime, nullable=False)
    date_to = db.Column(db.DateTime, nullable=False)
    resources = db.relationship('BookResource', backref='appointment', lazy=True)

    def __init__(self, date_from, date_to, resources = list()):
        self.date_from = date_from
        self.date_to = date_to
        self.resources = resources





