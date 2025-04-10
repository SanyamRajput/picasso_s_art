from app import db, User, Artwork, Comment
from datetime import datetime

def insert_sample_data():
    # Check if data already exists
    if User.query.count() > 0:
        print("Data already exists in the database. Skipping insertion.")
        return

    # Create sample users
    users = [
        User(username='john_doe', password='password123', created_at=datetime.utcnow()),
        User(username='jane_smith', password='password456', created_at=datetime.utcnow()),
        User(username='artist_mike', password='password789', created_at=datetime.utcnow())
    ]
    
    for user in users:
        db.session.add(user)
    db.session.commit()
    print("Users created successfully!")
    
    # Create sample artworks
    artworks = [
        Artwork(
            title='Sunset Over Mountains',
            description='A beautiful landscape painting of mountains at sunset',
            filename='sunset.jpg',
            upload_date=datetime.utcnow(),
            user_id=users[0].id
        ),
        Artwork(
            title='Abstract Harmony',
            description='An abstract painting with vibrant colors',
            filename='abstract.jpg',
            upload_date=datetime.utcnow(),
            user_id=users[1].id
        ),
        Artwork(
            title='City Lights',
            description='A night scene of a bustling city',
            filename='city.jpg',
            upload_date=datetime.utcnow(),
            user_id=users[2].id
        )
    ]
    
    for artwork in artworks:
        db.session.add(artwork)
    db.session.commit()
    print("Artworks created successfully!")
    
    # Create sample comments
    comments = [
        Comment(
            content='This is absolutely stunning!',
            created_at=datetime.utcnow(),
            user_id=users[1].id,
            artwork_id=artworks[0].id
        ),
        Comment(
            content='The colors are so vibrant!',
            created_at=datetime.utcnow(),
            user_id=users[2].id,
            artwork_id=artworks[1].id
        ),
        Comment(
            content='Great composition!',
            created_at=datetime.utcnow(),
            user_id=users[0].id,
            artwork_id=artworks[2].id
        )
    ]
    
    for comment in comments:
        db.session.add(comment)
    db.session.commit()
    print("Comments created successfully!")
    
    print("\nSample data inserted successfully!")

if __name__ == '__main__':
    insert_sample_data() 