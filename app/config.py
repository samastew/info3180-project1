import os
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.

class Config(object):
    """Base Config Object"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', 'postgresql://username:password@localhost/databasename')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Folder where uploaded property photos will be saved
    UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'uploads')
    
    # Maximum file size for uploads (16MB)
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024
    
    # Allowed image extensions for property photos
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}