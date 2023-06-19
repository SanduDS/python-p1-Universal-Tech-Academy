import os

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or b'>\xfc\xb0\xa3[\x90\x11cX\x99@\xe0\xee3~\xcd'
    MONGODB_SETTINGS = { 'db' : 'UTA_Enrollment' }