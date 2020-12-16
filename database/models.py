import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, String, Integer, Date
import json


db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

database_connection = os.environ['DATABASE_URL'] if os.environ[
    'TEST'] == 'False' else os.environ['TEST_DATABASE_URL']


def setup_db(app, database_path=database_connection):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


'''
db_drop_and_create_all()
    drops the database tables and starts fresh
    can be used to initialize a clean database
'''


def db_drop_and_create_all():
    db.drop_all()
    db.create_all()


'''
Extend the base Model class to add common methods
'''


class DatabaseOperations(db.Model):
    __abstract__ = True

    def insert(self):
        db.session.add(self)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def update(self):
        db.session.commit()


class Actor(DatabaseOperations):
    __tablename__ = 'actors'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    age = db.Column(db.Integer)
    gender = db.Column(db.String(10))

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def format(self):
        return {"name": self.name, "age": self.age, "gender": self.gender}


class Movie(DatabaseOperations):
    __tablename__ = 'movies'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(80))
    release_date = db.Column(db.Date)

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def format(self):
        return {"title": self.title, "release_date": self.release_date}
