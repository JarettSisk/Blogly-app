"""Blogly application."""

# Imports
from flask import Flask, request, render_template, redirect, flash, session, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User, Post, Tag, PostTag
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
    USERS = User.query.all()
    TAGS = Tag.query.all()
    return render_template('users.html', users=USERS, tags=TAGS)

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
    

    # Deleting the user
    user = User.query.get_or_404(userid)
    db.session.delete(user)
    db.session.commit()
    return redirect('/users')

# Routes for user posts
@app.route('/posts/<post_id>')
def view_post(post_id):
    postid = int(post_id)
    POST = Post.query.get_or_404(postid)
    TAGS = POST.tags
    return render_template('post.html', post=POST, tags=TAGS)

@app.route('/posts/<post_id>/delete')
def delete_post(post_id):
    """Delete a post"""
    postid = int(post_id)
    POST = Post.query.get_or_404(postid)
    # Checking that post exists
    # post_tags = PostTag.query.filter(PostTag.post_id == postid).delete()
    

    # match = Post.query.filter(Post.id == postid).delete()
    # if match != 0 and POST != 0:
    db.session.delete(POST)
    db.session.commit()
    return redirect(f'/users/{POST.user_id}')
    # else:
    #     abort(404, f"Could not delete the post with the id of {postid}")

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

    # Get available tags
    TAGS = Tag.query.all()
    if request.method == 'POST':
        
        title = request.form.get('title-input')
        content = request.form.get('content-input')
        

        # Tags 
        tag_ids = [int(num) for num in request.form.getlist("tag-checkboxes")]
        tags = Tag.query.filter(Tag.id.in_(tag_ids)).all()

        new_post = Post(title = title, content = content, user_id = userid, tags=tags)

        db.session.add(new_post)
        db.session.commit()

        return redirect(f'/users/{userid}')
    elif request.method == "GET":
        return render_template('new-post.html', user=USER, tags=TAGS)

# Routes for tags
@app.route('/tags')
def get_tags_list():
    """Fetch all the tags from the db"""
    TAGS = Tag.query.all()
    return render_template('tags.html', tags=TAGS)

@app.route('/tags/<tag_id>')
def get_tag_info(tag_id):
    """Get tag with the matching id and get posts that use the tag"""

    # Convert to int
    tagid = int(tag_id)
    # Get the tag instance
    TAG = Tag.query.get(tagid)
    # Get the posts that use the tag
    POSTS = TAG.posts
    return render_template('tag.html', tag=TAG, posts=POSTS)

@app.route('/tags/new', methods=['GET', 'POST'])
def create_new_tag():
    if request.method == 'POST':
        
        name = request.form.get('name-input')

        new_tag = Tag(name=name)
        db.session.add(new_tag)
        db.session.commit()

        return redirect(f'/tags')
    elif request.method == "GET":
        TAGS = Tag.query.all()
        return render_template('new-tag.html', tags=TAGS)

@app.route('/tags/<tag_id>/edit', methods=['GET','POST'])
def edit_tag(tag_id):
    """Edit a tag"""
    # Converting path variable to type integer
    tagid = int(tag_id)
    # Getting back the correct user based on user_id\
    TAG = Tag.query.get_or_404(tagid)

    if request.method == 'POST':
        
        name = request.form.get('name-input')

        TAG.name = name
        db.session.commit()
        return redirect(f'/tags/{tagid}')
    elif request.method == "GET":
        
        return render_template('edit-tag.html', tag=TAG )

@app.route('/tags/<tag_id>/delete')
def delete_tag(tag_id):
    """Delete a tag"""
    tagid = int(tag_id)
    TAG = Tag.query.get_or_404(tagid)
    # match = Tag.query.filter(Tag.id == tagid).delete()
    db.session.delete(TAG)
    db.session.commit()
    return redirect(f'/tags')

