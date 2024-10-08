import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret')
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URL', 'sqlite:///my_database.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
