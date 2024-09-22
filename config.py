# config.py
import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'jimmy'
    DATABASE = 'track_it.db'