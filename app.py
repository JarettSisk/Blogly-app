"""Blogly application."""

# Imports
import re
from flask import Flask, request, render_template, redirect, flash, session, abort
from flask_debugtoolbar import DebugToolbarExtension
from models import db, connect_db, User

app = Flask(__name__)
app.debug = True
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
    return render_template('user.html', user=USER)

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

    # Checking that user exists
    match = User.query.filter(User.id == userid).delete()
    if match != 0:
        db.session.commit()
        return redirect('/users')
    else:
        abort(404, f"Could not delete the user with the id of {userid}")

