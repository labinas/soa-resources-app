from xmlrpc.client import DateTime
import app
from dataclasses import dataclass
import enum
import sqlalchemy


class ResourceType(enum.Enum):
    ROOM = 1
    FOOD = 2
    TOYS = 3
    MEDICATION = 4

resource_type = app.db.Enum(ResourceType, name='resource_type_enum')

class Resource(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    name = app.db.Column(app.db.String(100), nullable=False)
    type = app.db.Column(resource_type, default=ResourceType.FOOD)

    def __init__(self, name, type):
        self.name = name
        self.type = type

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'type': self.type
        }

#Schema
class ResourceSchema(app.ma.Schema):
    class Meta:
        fields = ('id', 'name', 'type')

resource_schema = ResourceSchema()
resources_schema = ResourceSchema(many=True)


class BookResource(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    resource_id = app.db.Column(app.db.Integer, app.db.ForeignKey('resource.id'), nullable=False)
    appointment_id = app.db.Column(app.db.Integer, app.db.ForeignKey('appointment.id'), nullable=False)
    quantity = app.db.Column(app.db.Integer, nullable=False)


    def __init__(self, resource_id, quantity):
        self.resource_id = resource_id
        self.quantity = quantity

    @property
    def serialize(self):
        return {
            'id': self.id,
            'resource_id': self.resource_id,
            'quantity': self.quantity
        }

#Schema
class BookResourceSchema(app.ma.Schema):
    class Meta:
        fields = ('id', 'resource_id', 'quantity')

bookResource_schema = BookResourceSchema()
bookResources_schema = BookResourceSchema(many=True)


class Appointment(app.db.Model):
    id = app.db.Column(app.db.Integer, primary_key=True)
    date_from = app.db.Column(app.db.DateTime, nullable=False)
    date_to = app.db.Column(app.db.DateTime, nullable=False)
    resources = app.db.relationship('BookResource', backref='appointment', lazy=True)

    def __init__(self, date_from, date_to, resources = list()):
        self.date_from = date_from
        self.date_to = date_to
        self.resources = resources

    @property
    def serialize(self):
        return {
            'id': self.id,
            'date_from': self.date_from,
            'date_to': self.date_to,
            'resources': [resource.serialize for resource in self.resources]
        }

#Schema
class AppointmentSchema(app.ma.Schema):
    class Meta:
        fields = ('id', 'date_from', 'date_to', 'resources')

appointment_schema = AppointmentSchema()
appointemts_schema = AppointmentSchema(many=True)


@dataclass
class ResourceDto:
    name: str
    resourceType: ResourceType

@dataclass
class BookResourceDto:
    resourceId: int
    quantity: int

@dataclass
class AppointmentDto:
    date_from: DateTime
    date_to: DateTime
    resources: list()







