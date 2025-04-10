from models import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    
    # Relationships
    artworks = db.relationship('Artwork', backref='user', lazy=True, cascade="all, delete-orphan")
    comments = db.relationship('Comment', backref='author', lazy=True, cascade="all, delete-orphan")
    
    # Many-to-many relationships
    liked_artworks = db.relationship(
        'Artwork',
        secondary='likes',
        backref=db.backref('liked_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    favorite_artworks = db.relationship(
        'Artwork',
        secondary='favorites',
        backref=db.backref('favorited_by', lazy='dynamic'),
        lazy='dynamic'
    )
    
    def __repr__(self):
        return f'<User {self.username}>' 