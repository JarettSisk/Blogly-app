#  Blogly database seed for initial setup.
import sys
sys.path.append('../../')

from models import User, Post, Tag, PostTag, db
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
db.session.add_all([post1, post2])
db.session.commit()

tag1 = Tag(name="comedy")
tag2 = Tag(name="news")
db.session.add_all([tag1, tag2])
db.session.commit()


post_tag1 = PostTag(post_id=1, tag_id=1)
post_tag2 = PostTag(post_id=2, tag_id=1)
post_tag3 = PostTag(post_id=2, tag_id=2)

db.session.add_all([post_tag1, post_tag2, post_tag3])
db.session.commit()


