import json
import os
from functools import wraps

import requests
from app import app, db
from flask import redirect, render_template, request, session


def requires_auth(f):
  @wraps(f)
  def decorated(*args, **kwargs):
    if 'profile' not in session:
      # Redirect to Login page here
      return redirect('/')
    return f(*args, **kwargs)

  return decorated


@app.route('/')
def index():
    return render_template('home.html')

@app.route('/login')
def login():
    context = {
        'auth0_client_id': os.environ.get('AUTH0_CLIENT_ID'),
        'auth0_domain': os.environ.get('AUTH0_DOMAIN'),
        'auth0_callback_url': os.environ.get('AUTH0_CALLBACK_URL')
    }
    return render_template('login.html', context=context)

@app.route('/user/<id>')
@requires_auth
def user_details(id):
    # show the user profile for that user
    context = {
        'user_id': id,
        'profile': session['profile']
    }
    return render_template('profile.html', context=context)


# Handle the Auth0 Callback
# See ref: https://auth0.com/docs/quickstart/webapp/python
@app.route('/callback')
def callback_handling():
  code = request.args.get('code')

  json_header = {'content-type': 'application/json'}

  token_url = "https://{domain}/oauth/token".format(domain=os.environ.get('AUTH0_DOMAIN'))

  token_payload = {
    'client_id':     os.environ.get('AUTH0_CLIENT_ID'),
    'client_secret': os.environ.get('AUTH0_CLIENT_SECRET'),
    'redirect_uri':  os.environ.get('AUTH0_CALLBACK_URL'),
    'code':          code,
    'grant_type':    'authorization_code'
  }

  token_info = requests.post(token_url, data=json.dumps(token_payload), headers = json_header).json()

  user_url = "https://{domain}/userinfo?access_token={access_token}" \
      .format(domain=os.environ.get('AUTH0_DOMAIN'), access_token=token_info['access_token'])

  user_info = requests.get(user_url).json()

  print user_info

  # We're saving all user information into the session
  session['profile'] = user_info

  # Redirect to the User logged in page that you want here
  return redirect('/user/1')
