"""Models for Blogly."""
from datetime import datetime
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
    """User Model"""
    # Table setup
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(20), nullable=False, unique=True)
    last_name = db.Column(db.String(20), nullable=True)
    image_url = db.Column(db.String, default='https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80')
    # End table setup

    # SQLALCHEMY relationships
    pposts = db.relationship("Post", backref="user", cascade="all, delete-orphan")

    # Instance methods
    def __repr__(self):
        return f"first_name = {self.first_name}, last_name = {self.last_name}, image_url = {self.image_url}"

class Post(db.Model):
    """Post model"""
    # Table setup
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(25), nullable=False)
    content = db.Column(db.String, nullable=False)
    created_at = db.Column(db.String, nullable=False, default=f'{datetime.now()}')
    # Relationship
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    
    

    def __repr__(self):
        return f'title: {self.title}, content: {self.content}, user_id: {self.user_id}, created_at: {self.created_at}'

class Tag(db.Model):
    """Tag model"""
    # Table setup
    __tablename__ = "tags"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String, nullable=False)

    # Example of a 'through' relationship
    posts = db.relationship('Post', secondary='posts_tags', cascade="all, delete", backref="tags" )

    def __repr__(self):
        return f'id: {self.id}, name: {self.name}'

class PostTag(db.Model):
    """Post + Tag many to many model"""
    # Table setup
    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey("posts.id"), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey("tags.id"), primary_key=True)

    def __repr__(self):
        return f'post id {self.post_id}, tag id: {self.tag_id}'


