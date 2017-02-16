import os
from os.path import join, dirname, abspath

from dotenv import load_dotenv

# load dotenv
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# App details
BASE_DIRECTORY = abspath(dirname(__file__))
DEBUG = True
SECRET_KEY = os.environ.get('SECRET_KEY')

# Database details
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = '{0}{1}'.format('sqlite:///',
                                          join(BASE_DIRECTORY, 'app.db'))