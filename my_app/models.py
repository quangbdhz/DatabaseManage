from my_app import db
from flask_login import UserMixin
from datetime import datetime
from flask_login.mixins import *

class Users(db.Model, UserMixin):
    Id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    FullName = db.Column(db.String(length=200), nullable=True)
    UserName = db.Column(db.String(length=100), nullable=True, unique=True)
    Password = db.Column(db.String(length=200), nullable=False)
    Email = db.Column(db.String(length=200), nullable=False, unique=True)
    Phone = db.Column(db.String(length=20), nullable=True)
    IsAdmin = db.Column(db.Integer(), nullable=False)
    IsDelete = db.Column(db.Integer(), nullable=False, default = 0)
    Active = db.Column(db.Integer(), nullable=False)
    Avatar = db.Column(db.String(length=200), nullable=True)

    def get_id(self):
        try:
            return text_type(self.Id)
        except AttributeError:
            raise NotImplementedError('No `id` attribute - override `get_id`')

class UserCreateDatabase(db.Model):
    __tablename__ = "UserCreateDatabase"
    Id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Name = db.Column(db.String(length=200), nullable=False)
    IdUserCreate = db.Column(db.Integer(), nullable=False)
    CreateDate = db.Column(db.DateTime, nullable=False, default=datetime.now())
    Active = db.Column(db.Integer(), nullable=False)

class Datatype(db.Model):
    __tablename__ = "Datatype"
    Id = db.Column(db.Integer(), primary_key=True, autoincrement=True)
    Name = db.Column(db.String(length=50), nullable=False)
    CheckInputNumber = db.Column(db.Integer(), nullable=False)
    Active = db.Column(db.Integer(), nullable=False)
