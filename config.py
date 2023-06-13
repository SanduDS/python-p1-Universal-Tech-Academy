import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'sandu'
    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }