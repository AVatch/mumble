from flask import g, render_template, redirect, request, session, url_for

from app import app, db

@app.route('/')
def index():
    return render_template('home.html')

@app.route('/user/<id>')
def user_details(id):
    # show the user profile for that user
    context = {
        'user_id': id
    }
    return render_template('profile.html', context=context)