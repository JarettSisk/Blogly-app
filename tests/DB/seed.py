#  Blogly database seed for initial setup.
import sys
sys.path.append('../../')

from models import User, Post, db
from app import app

# Create all tables
db.drop_all()
db.create_all()

user1 = User(first_name='John', last_name='Doe')
user2 = User(first_name='Steve', last_name='Marks')
db.session.add_all([user1, user2])
db.session.commit()

post1 = Post(title='Test post 1', content='Hey there, this is a test post', user_id=1)
post2 = Post(title='Test post 2', content='Hey there, this is a test post', user_id=1)
post3 = Post(title='Test post 3', content='Hey there, this is a test post', user_id=2)
post4 = Post(title='Test post 4', content='Hey there, this is a test post', user_id=2)
db.session.add_all([post1, post2, post3, post4])
db.session.commit()

