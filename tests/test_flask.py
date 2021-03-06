from unittest import TestCase
import sys
sys.path.append('../')
from app import app
from models import db, User, Post

# Use test database and don't clutter tests with SQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly_test'
app.config['SQLALCHEMY_ECHO'] = False

# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']

db.drop_all()
db.create_all()

class UserViewsTestCase(TestCase):
    """Tests for views for users."""

    def setUp(self):
        """Add sample user."""

        # Delete all users and posts
        Post.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()
        
        user = User(first_name="TestUser", last_name="Testing", image_url='https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80')

        db.session.add(user)
        db.session.commit()

        self.userid = user.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_users(self):
        """Check for list of users"""
        with app.test_client() as client:
            res = client.get("/users")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('TestUser', html)

    def test_show_user_details(self):
        """Check for details in user page"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.userid}")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('<h2>TestUser Testing</h2>', html)

    def test_add_user(self):
        """Checks that a user is added"""
        with app.test_client() as client:
            d = {"first-name-input": "TestUser2", "last-name-input": "Testing2", "image-url-input": 'https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80'}
            
            res = client.post("/users/new", data=d, follow_redirects=True)
            
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUser2", html)

    def test_edit_user(self):
        """Tests that a user gets edited"""
        with app.test_client() as client:
            d = {"first-name-input": "TestUser3", "last-name-input": "Testing3", "image-url-input": 'https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80'}
            
            res = client.post(f"/users/{self.userid}/edit", data=d, follow_redirects=True)
            
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("TestUser3", html)

    def test_delete_user(self):
        """Test that a user gets deleted"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.userid}/delete")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
            self.assertNotIn('TestUser', html)
    
    def test_delete_user_error(self):
        """If a user with the given id is not found, send 404"""
        with app.test_client() as client:
            res = client.get("/users/999/delete")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 404)
            self.assertIn('Could not delete the user with the id of 999', html)




class PostViewsTestCase(TestCase):
    """Tests for views for Posts."""

    def setUp(self):
        """Add sample user. and posts"""

        # Delete all users and posts
        Post.query.delete()
        db.session.commit()
        User.query.delete()
        db.session.commit()
        
        user = User(first_name="TestUser", last_name="Testing", image_url='https://images.unsplash.com/photo-1586410073908-5f314173d3a5?ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&ixlib=rb-1.2.1&auto=format&fit=crop&w=675&q=80')

        db.session.add(user)
        db.session.commit()
        self.userid = user.id


        post = Post(title='Test Title', content='Test content', user_id=self.userid)
        db.session.add(post)
        db.session.commit()

        self.postid = post.id

    def tearDown(self):
        """Clean up any fouled transaction."""

        db.session.rollback()


    def test_list_posts(self):
        """Check for list of posts"""
        with app.test_client() as client:
            res = client.get(f"/users/{self.userid}")
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Test Title', html)

    def test_show_post_details(self):
        """Check for details in post page"""
        with app.test_client() as client:
            res = client.get(f"/posts/{self.postid}")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 200)
            self.assertIn('Test content', html)

    def test_add_post(self):
        """Checks that a post is added"""
        with app.test_client() as client:
            d = {"title-input": "Test Title 2", "content-input": "Test content 2"}
            
            res = client.post(f"/users/{self.userid}/posts/new", data=d, follow_redirects=True)
            
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test Title 2", html)

    def test_edit_post(self):
        """Tests that a post gets edited"""
        with app.test_client() as client:
            d = {"title-input": "Test Title 3", "content-input": "Test content 3"}
            
            res = client.post(f"/posts/{self.postid}/edit", data=d, follow_redirects=True)
            
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn("Test Title 3", html)

    def test_delete_post(self):
        """Test that a post gets deleted"""
        with app.test_client() as client:
            res = client.get(f"/posts/{self.postid}/delete")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 302)
            self.assertNotIn('Test Title 3', html)
    
    def test_delete_post_error(self):
        """If a user with the given id is not found, send 404"""
        with app.test_client() as client:
            res = client.get("/posts/999/delete")
            html = res.get_data(as_text=True)
            self.assertEqual(res.status_code, 404)
            self.assertIn('Could not delete the post with the id of 999', html)