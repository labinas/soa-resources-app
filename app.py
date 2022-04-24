from email.mime import base
from ntpath import join
from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy 
from flask_marshmallow import Marshmallow
from dotenv import load_dotenv
import os

#Init app
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
env = join(basedir, '.env')
env_local = join(basedir, '.env.local')

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

#Init DB
db = SQLAlchemy(app)
#Init MA
ma = Marshmallow(app)


#Run server 
if __name__ == '__main__':
    app.run(debug=True)

