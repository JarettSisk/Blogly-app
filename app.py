"""Blogly application."""

# Imports
from flask import Flask, request, render_template, redirect, flash, session, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post
from datetime import datetime

app = Flask(__name__)
# Debugging turned off
app.debug = False
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'MySecretKey123'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

toolbar = DebugToolbarExtension(app)

connect_db(app)

# Routes
@app.route('/')
def redirect_to_users_list():
    return redirect('/users')

@app.route('/users')
def list_users():
    """Shows list of all users in the database"""
    USERS = User.query.all();
    return render_template('users.html', users=USERS)

@app.route('/users/new', methods=['GET', 'POST'])
def creat_new_user():
    """Creates a new user"""
    if request.method == 'POST':
        firstName = request.form.get('first-name-input')
        lastName = request.form.get('last-name-input')
        imageUrl = request.form.get('image-url-input')

        new_user = User(first_name = firstName, last_name = lastName, image_url = imageUrl)
        db.session.add(new_user)
        db.session.commit()

        return redirect('/users')
    elif request.method == "GET":
        return render_template('signup.html')

@app.route('/users/<user_id>')
def show_user_info(user_id):
    """Shows details of a specific user"""
    # Converting path variable to type integer
    userid = int(user_id)
    # Getting back the correct user based on user_id
    USER = User.query.get_or_404(userid)
    POSTS = Post.query.filter_by(user_id=userid)
    return render_template('user.html', user=USER, posts=POSTS)

@app.route('/users/<user_id>/edit', methods=['GET','POST'])
def edit_user(user_id):
    """Edit the user"""
    # Converting path variable to type integer
    userid = int(user_id)
    # Getting back the correct user based on user_id\
    USER = User.query.get_or_404(userid)

    if request.method == 'POST':
        
        firstName = request.form.get('first-name-input')
        lastName = request.form.get('last-name-input')
        imageUrl = request.form.get('image-url-input')

        USER.first_name = firstName
        USER.last_name = lastName
        USER.image_url = imageUrl
        db.session.commit()
        return redirect('/users')
    elif request.method == "GET":
        
        return render_template('edit-user.html', user=USER )

@app.route('/users/<user_id>/delete')
def delete_user(user_id):
    """Delete the user"""
    userid = int(user_id)
    # Deleting all the posts from that user
    POSTS = Post.query.filter(Post.user_id == userid).delete()
    if POSTS != 0:
        db.session.commit()

    # Deleting the user
    user = User.query.filter(User.id == userid).delete()
    if user != 0:
        db.session.commit()
        return redirect('/users')
    else:
        abort(404, f"Could not delete the user with the id of {userid}")

# Routes for user posts
@app.route('/posts/<post_id>')
def view_post(post_id):
    postid = int(post_id)

    POST = Post.query.get_or_404(postid)
    return render_template('post.html', post=POST)

@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    """Delete a post"""
    postid = int(post_id)
    POST = Post.query.get(postid)
    # Checking that post exists
    match = Post.query.filter(Post.id == postid).delete()
    if match != 0 and POST != 0:
        db.session.commit()
        return redirect(f'/users/{POST.user_id}')
    else:
        abort(404, f"Could not delete the post with the id of {postid}")

@app.route('/posts/<post_id>/edit', methods=['GET','POST'])
def edit_post(post_id):
    """Edit a post"""
    # Converting path variable to type integer
    postid = int(post_id)
    # Getting back the correct user based on user_id\
    POST = Post.query.get_or_404(postid)

    if request.method == 'POST':
        
        title = request.form.get('title-input')
        content = request.form.get('content-input')

        POST.title = title
        POST.content = content
        POST.created_at = f'{datetime.now()}'
        db.session.commit()
        return redirect(f'/users/{POST.user_id}')
    elif request.method == "GET":
        
        return render_template('edit-post.html', post=POST )

@app.route('/users/<user_id>/posts/new', methods=['GET', 'POST'])
def creat_new_post(user_id):
    """Creates a new post"""
    userid = int(user_id)
    # Get the user
    USER = User.query.get_or_404(userid)
    if request.method == 'POST':
        
        title = request.form.get('title-input')
        content = request.form.get('content-input')

        new_post = Post(title = title, content = content, user_id = userid)
        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{userid}')
    elif request.method == "GET":
        return render_template('new-post.html', user=USER)