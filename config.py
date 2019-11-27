import os
from dotenv import load_dotenv
load_dotenv()




class Config(object):
  DEBUG=True
  SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL')
  SECRET_KEY='supersecret'
  FLASK_ADMIN_SWATCH = 'cerulean'
  EMAIL_API=os.environ.get('EMAIL_API')