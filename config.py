# Import required modules
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get the base directory
basedir = os.path.abspath(os.path.dirname(__file__))

# Configuration class to hold application settings
class Configuration(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your_default_secret_key'
    SQLALCHEMY_DATABASE_URI = 'sqlite:///investpro.db'  # Set the database URI to work with SQLite and set the database name
    SQLALCHEMY_TRACK_MODIFICATIONS = False   # Disable modification tracking