from flask_login import UserMixin
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

user_stack = db.Table('bridge',
    db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('stack_id',db.Integer,db.ForeignKey('stacks.id'))
)

user_file = db.Table('files',
    db.Column('user_id',db.Integer,db.ForeignKey('users.id')),
    db.Column('file_id',db.Integer,db.ForeignKey('filer.id'))
)

class Users(UserMixin,db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(255))
    following = db.relationship('Stacks',secondary=user_stack,backref='stack list')
    folls = db.relationship('Filer',secondary=user_file,backref='file list')


class Stacks(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    stack_name = db.Column(db.String(255),unique=True)
    last_cve = db.Column(db.String(255),unique=True)


class Filer(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    file_name = db.Column(db.String(255))
    data = db.Column(db.LargeBinary)

