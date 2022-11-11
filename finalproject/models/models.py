from werkzeug.security import generate_password_hash, check_password_hash
from .db import db
from datetime import datetime


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    google_name = db.Column(db.String(255), nullable=True, unique=True)
    balance = db.Column(db.Integer)
    user_post = db.relationship("Post", back_populates = "owner", cascade="all, delete-orphan")
    projects = db.relationship("Project", back_populates="user")
    pledges = db.relationship("Pledge", back_populates="user")
    
    def to_dict(self):
        return {
            "id": self.id,
            # "firstname": self.firstname,
            # "lastname": self.lastname,
            "username": self.username,
            "email": self.email
        }
class Post(db.Model):
    __tablename__="posts"
    post_id = db.Column(db.Integer, primary_key=True)
    titlename=db.Column(db.String(100), nullable=False)
    fundraising=db.Column(db.Text, nullable=False)
    additional = db.Column(db.String(100), nullable=False)
    fromfund = db.Column(db.Integer,nullable = True)
    tofund =db.Column(db.Integer,nullable=False)
    post_owner = db.Column(db.Integer, db.ForeignKey('users.id'),nullable=False)
    owner = db.relationship("User", back_populates="user_post")
    def repr(self):
        return f'<User {self.post_id}>'


class Pledge(db.Model):
    __tablename__ = "pledges"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    project_id = db.Column(db.Integer, db.ForeignKey(
        "projects.id"), nullable=False)
    amount = db.Column(db.Numeric(10, 2), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.relationship("User", back_populates="pledges")
    project = db.relationship("Project", back_populates="pledges")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "amount": float(self.amount),
            "created_at": self.created_at,
            "updated_at": self.updated_at
        }

    def to_dict_projects(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "project_id": self.project_id,
            "amount": float(self.amount),
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "project": self.project.to_dict()
        }


class Project(db.Model):
    __tablename__ = 'projects'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    funding_goal = db.Column(db.Numeric(10, 2), nullable=False)
    balance = db.Column(db.Numeric(10, 2), nullable=False, default=0.00)
    date_goal = db.Column(db.Date, nullable=False)
    category = db.Column(db.String, nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.now())
    updated_at = db.Column(db.DateTime, nullable=False, default=datetime.now())

    user = db.relationship("User", back_populates="projects")
    pledges = db.relationship(
        "Pledge", back_populates="project", cascade="delete, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
            "title": self.title,
            "description": self.description,
            "funding_goal": float(self.funding_goal),
            "balance": float(self.balance),
            "date_goal": self.date_goal.isoformat(),
            "category": self.category,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "user": self.user.to_dict()
        }
