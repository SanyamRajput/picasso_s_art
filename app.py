from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from datetime import datetime
import os
from werkzeug.utils import secure_filename
import pymysql
import getpass
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps

# Import models
from models import db, User, Artwork, Comment

# Use PyMySQL instead of MySQLdb
pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key-here'  # Change this to a secure secret key
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Create uploads directory if it doesn't exist
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Database configuration
db_user = 'root'
db_password = 'sanyam'
db_host = 'localhost'
db_name = 'art_gallery'

# Create database if it doesn't exist
conn = pymysql.connect(
    host=db_host,
    user=db_user,
    password=db_password
)
cursor = conn.cursor()
cursor.execute(f"CREATE DATABASE IF NOT EXISTS {db_name}")
conn.close()

# Configure SQLAlchemy
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql://{db_user}:{db_password}@{db_host}/{db_name}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database with the app
db.init_app(app)

# Login required decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'error')
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    artworks = Artwork.query.order_by(Artwork.upload_date.desc()).all()
    return render_template('index.html', artworks=artworks)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if User.query.filter_by(username=username).first():
            flash('Username already exists. Please choose another one.', 'error')
            return redirect(url_for('register'))
        
        user = User(
            username=username,
            password=generate_password_hash(password),
            created_at=datetime.utcnow()
        )
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user_id'] = user.id
            session['username'] = user.username
            flash('Logged in successfully!', 'success')
            return redirect(url_for('index'))
        
        flash('Invalid username or password.', 'error')
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully!', 'success')
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    user = User.query.get(session['user_id'])
    return render_template('profile.html', user=user)

@app.route('/upload', methods=['GET', 'POST'])
@login_required
def upload():
    if request.method == 'POST':
        if 'artwork' not in request.files:
            flash('No file selected', 'error')
            return redirect(request.url)
        
        file = request.files['artwork']
        if file.filename == '':
            flash('No file selected', 'error')
            return redirect(request.url)
        
        if file:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            artwork = Artwork(
                title=request.form['title'],
                description=request.form['description'],
                filename=filename,
                user_id=session['user_id']
            )
            db.session.add(artwork)
            db.session.commit()
            
            flash('Artwork uploaded successfully!', 'success')
            return redirect(url_for('index'))
    
    return render_template('upload.html')

@app.route('/artwork/<int:artwork_id>')
def artwork_detail(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    return render_template('artwork_detail.html', artwork=artwork)

@app.route('/artwork/<int:artwork_id>/like', methods=['POST'])
@login_required
def like_artwork(artwork_id):
    user = User.query.get(session['user_id'])
    artwork = Artwork.query.get_or_404(artwork_id)
    
    if artwork in user.liked_artworks:
        user.liked_artworks.remove(artwork)
        liked = False
    else:
        user.liked_artworks.append(artwork)
        liked = True
    
    db.session.commit()
    
    return jsonify({'liked': liked, 'likes_count': len(artwork.liked_by.all())})

@app.route('/artwork/<int:artwork_id>/favorite', methods=['POST'])
@login_required
def favorite_artwork(artwork_id):
    user = User.query.get(session['user_id'])
    artwork = Artwork.query.get_or_404(artwork_id)
    
    if artwork in user.favorite_artworks:
        user.favorite_artworks.remove(artwork)
        favorited = False
    else:
        user.favorite_artworks.append(artwork)
        favorited = True
    
    db.session.commit()
    
    return jsonify({'favorited': favorited})

@app.route('/artwork/<int:artwork_id>/comment', methods=['POST'])
@login_required
def add_comment(artwork_id):
    content = request.form.get('content')
    if not content:
        flash('Comment cannot be empty', 'error')
        return redirect(url_for('artwork_detail', artwork_id=artwork_id))
    
    artwork = Artwork.query.get_or_404(artwork_id)
    
    comment = Comment(
        content=content,
        user_id=session['user_id'],
        artwork_id=artwork_id
    )
    
    db.session.add(comment)
    db.session.commit()
    
    flash('Comment added successfully!', 'success')
    return redirect(url_for('artwork_detail', artwork_id=artwork_id))

@app.route('/artwork/<int:artwork_id>/delete', methods=['POST'])
@login_required
def delete_artwork(artwork_id):
    artwork = Artwork.query.get_or_404(artwork_id)
    
    # Only allow the artwork owner to delete it
    if artwork.user_id != session['user_id']:
        flash('You do not have permission to delete this artwork.', 'error')
        return redirect(url_for('artwork_detail', artwork_id=artwork_id))
    
    # Delete the image file
    try:
        os.remove(os.path.join(app.config['UPLOAD_FOLDER'], artwork.filename))
    except:
        # If file doesn't exist, continue anyway
        pass
    
    # Delete the artwork from database (this will also delete associated comments due to cascade)
    db.session.delete(artwork)
    db.session.commit()
    
    flash('Artwork deleted successfully!', 'success')
    return redirect(url_for('index'))

if __name__ == '__main__':
    with app.app_context():
        # Create tables if they don't exist
        db.create_all()
        print("Database tables created successfully.")
    
    app.run(debug=True) 