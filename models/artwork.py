from models import db
from datetime import datetime

# Association tables
likes = db.Table('likes',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id'), primary_key=True)
)

favorites = db.Table('favorites',
    db.Column('user_id', db.Integer, db.ForeignKey('user.id'), primary_key=True),
    db.Column('artwork_id', db.Integer, db.ForeignKey('artwork.id'), primary_key=True)
)

class Artwork(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    filename = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    # Relationships
    comments = db.relationship('Comment', backref='artwork', lazy=True, cascade="all, delete-orphan")
    
    def __repr__(self):
        return f'<Artwork {self.title}>' 