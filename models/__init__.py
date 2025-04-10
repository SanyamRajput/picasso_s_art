from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Import models after db is defined to avoid circular imports
from models.user import User
from models.artwork import Artwork
from models.comment import Comment 