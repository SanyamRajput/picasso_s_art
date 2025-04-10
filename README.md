# PICASSO'S - Art Gallery Web Application

A web application for uploading and displaying artwork using Python, Flask, and MySQL.

## Features

- Upload artwork with title and description
- View all uploaded artwork in a responsive grid layout
- Like artwork to show appreciation
- Add comments to artwork
- Add artwork to favorites
- Modern and clean user interface using Bootstrap
- Secure file upload handling
- MySQL database for storing artwork information
- User authentication and profiles

## Prerequisites

- Python 3.6 or higher
- MySQL Server
- pip (Python package installer)

## Setup Instructions

1. **Clone the repository**:

   ```
   git clone <repository-url>
   cd picassos
   ```

2. **Create a virtual environment** (optional but recommended):

   ```
   python -m venv venv
   venv\Scripts\activate  # On Windows
   source venv/bin/activate  # On macOS/Linux
   ```

3. **Install dependencies**:

   ```
   pip install -r requirements.txt
   ```

4. **Run the application**:

   ```
   python app.py
   ```

   - When prompted, enter your MySQL root password
   - The application will automatically create the database and necessary tables
   - **Note**: The application will drop and recreate all tables on startup to ensure the schema is up-to-date

5. **Access the application**:
   - Open your web browser and go to `http://localhost:5000`

## Usage

- **View Artwork**: Visit the home page to see all uploaded artwork
- **Upload Artwork**: Click on "Upload Artwork" in the navigation bar to add new artwork
- **View Artwork Details**: Click on an artwork to view its details, like it, comment on it, or add it to favorites
- **Like Artwork**: Click the heart icon to like an artwork
- **Comment on Artwork**: Write a comment in the comment section of an artwork
- **Add to Favorites**: Click the star icon to add an artwork to your favorites
- **User Profiles**: Create an account to manage your artworks and interact with others
- **Supported Image Formats**: JPG, PNG, GIF (Max size: 16MB)

## Database Schema

The application uses the following database schema:

- **User**: Stores user information (id, username, password, created_at)
- **Artwork**: Stores artwork information (id, title, description, filename, upload_date, user_id)
- **Comment**: Stores comments on artwork (id, content, created_at, user_id, artwork_id)
- **Likes**: Association table for user-artwork likes (user_id, artwork_id)
- **Favorites**: Association table for user-artwork favorites (user_id, artwork_id)

## Troubleshooting

- If you encounter database connection issues:
  - Make sure MySQL is running
  - Verify that you're using the correct password for the root user
  - Check that your MySQL user has permissions to create databases
- For file upload issues, check that the `static/uploads` directory exists and has write permissions
- If you see errors about missing columns or tables, restart the application to ensure the database schema is up-to-date
