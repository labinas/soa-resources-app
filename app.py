from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
from json import JSONEncoder
import psycopg2
import os


#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
env = os.path.join(basedir, '.env')
env_local = os.path.join(basedir, '.env.local')

load_dotenv(env)
load_dotenv(env_local)

#Database
db_username = os.getenv('POSTGRES_USER')
db_password = os.getenv('POSTGRES_PASSWORD')
db_url = os.getenv('POSTGRES_URL_LOCAL')
db_name = os.getenv('POSTGRES_DB')
connection_url = 'postgresql+psycopg2://{username}:{password}@{url}/{name}'.format(username=db_username, password=db_password, url=db_url, name=db_name)
app.config['SQLALCHEMY_DATABASE_URI'] = connection_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
con = psycopg2.connect(
    user = db_username,
    password = db_password,
    host = 'localhost',
    database = db_name
)

#Init DB
db = SQLAlchemy(app)
#Init MA
ma = Marshmallow(app)

#Import models and schemas
#from models import Resource, BookResource, Appointment, ResourceType, ResourceDto, BookResourceDto, AppointmentDto
#from models import resource_schema, resources_schema, appointemts_schema, appointment_schema, bookResource_schema, bookResources_schema


#createResource
@app.route('/resource', methods=['POST'])
def create_resource():
    import models

    name = request.json['name']
    type = request.json['type']

    new_resource = models.Resource(name, type)

    db.session.add(new_resource)
    db.session.commit()

    return models.resource_schema.jsonify(new_resource)


#editResource
@app.route('/resource/<id>', methods=['PUT'])
def edit_resource(id):
    import models

    resource = models.Resource.query.get(id)

    name = request.json['name']
    type = request.json['type']

    resource.name = name
    resource.type = type

    db.session.commit()

    return models.resource_schema.jsonify(resource.serialize)


#deleteResource
@app.route('/resource/<id>', methods=['DELETE'])
def delete_resource(id):
    import models

    resource = models.Resource.query.get(id)

    db.session.delete(resource)
    db.session.commit()

    return models.resource_schema.jsonify(resource.serialize)


#getResource
@app.route('/resource/<id>', methods=['GET'])
def get_resource(id):
    import models

    resource = models.Resource.query.get(id)
    
    return models.resource_schema.jsonify(resource.serialize)


#getResources
@app.route('/resources', methods=['GET'])
def get_resources(id):
    import models

    resources = models.Resource.query.all()
    result = models.resources_schema.dump([resource.serialize for resource in resources])

    return jsonify(result)


#bookAppointment
@app.route('/appointment', methods=['POST'])
def book_appointment():
    import models

    date_from = request.json['date_from']
    date_to = request.json['date_to']
    resources = request.json['appointments']
    
    appointment = models.Appointment(date_from, date_to, resources)
    models.bookResource_schema.dump(resources)

    db.session.add(appointment)
    db.session.commit()

    return models.appointment_schema.jsonify(appointment)


#editAppointment
@app.route('/appointment/<id>', methods=['PUT'])
def edit_appointment(id):
    import models

    appointment = models.Appointment.query.get(id)
    date_from = request.json['date_from']
    date_to = request.json['date_to']
    resources = request.json['appointments']

    appointment.date_from = date_from
    appointment.date_to = date_to
    appointment.resources = resources

    models.bookResource_schema.dump(resources)

    db.session.commit()

    return models.appointment_schema.jsonify(appointment.serialize)


#cancelAppointment
@app.route('/appointment/<id>', methods=['DELETE'])
def cancel_appointment(id):
    import models

    appointment = models.Appointment.query.get(id)

    db.session.delete(appointment)
    db.session.commit()

    return models.appointment_schema.jsonify(appointment)


#getAppointment
@app.route('/appointment/<id>', methods=['GET'])
def get_appointment(id):
    import models

    appointment = models.Appointment.query.get(id)

    return models.appointment_schema.jsonify(appointment.serialize)



#getAppointments
@app.route('/appointments', methods=['GET'])
def get_appointments(id):
    import models

    appointments = models.Appointment.query.all()
    result = models.appointemts_schema.dump([appointment.serialize for appointment in appointments])

    return jsonify(result)


#Run server 
if __name__ == '__main__':
    app.run(debug=True)

