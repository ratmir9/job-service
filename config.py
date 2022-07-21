import os


SERVER_HOST = os.getenv('SERVER_HOST', '127.0.0.1')
SERVER_PORT = os.getenv('SERVER_PORT', 5000)

DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_USER = os.getenv('DB_USER', 'postgres')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_NAME = os.getenv('DB_NAME', 'fast')

JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'you-secret-key')
JWT_ALGORITHM=os.getenv('JWT_ALGORIHM','HS256')
JWT_EXPIRATION = 3 * 60 * 60 

class Config:
  DEBUG = True
  SQLALCHEMY_DATABASE_URI = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
  SQLALCHEMY_TRACK_MODIFICATIONS = False
  JSON_AS_ASCII = False
