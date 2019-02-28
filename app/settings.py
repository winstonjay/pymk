import os

from dotenv import load_dotenv
load_dotenv()

SECRET_KEY = os.getenv('APP_SECRET_KEY')

# Database - SQL Alchemy
SQLALCHEMY_DATABASE_URI = 'sqlite:///model.db'
SQLALCHEMY_TRACK_MODIFICATIONS = False

# Google Auth
GA_CLIENT_ID = os.getenv('GA_CLIENT_ID')
GA_CLIENT_SECRET = os.getenv('GA_CLIENT_SECRET')