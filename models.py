"""Models for Blogly."""
# import sqlalchemy
from enum import unique
from flask_sqlalchemy import SQLAlchemy

# Set up db connection
db = SQLAlchemy()

def connect_db(app):
    db.app = app
    db.init_app(app)

# User class
class User(db.Model):
    """User"""
    # Table setup
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    first_name = db.Column(db.String(20), nullable=False, unique=True)

    last_name = db.Column(db.String(20), nullable=True)

    image_url = db.Column(db.String, default='https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80')
    # End table setup

    # Instance methods
    def __repr__(self):
        return f"first_name = {self.first_name}, last_name = {self.last_name}, image_url = {self.image_url}"


