from flask import g, render_template, redirect, request, session, url_for

from app import app, db

@app.route('/')
def index():
    return render_template('index.html')