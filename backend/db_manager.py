from flask_sqlalchemy import SQLAlchemy
import datetime
from __init__ import db

class UploadedFiles(db.Model):

    __tablename__ = 'uploads'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    filename = db.Column(db.String(255), nullable=False)
    file_content = db.Column(db.Text, nullable=False)  # Store file content as text
    uploaded_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<UploadedFile {self.filename}>"
    
class ChatRecord(db.Model):

    __tablename__ = 'ChatRecord'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # Unique ID
    user_id = db.Column(db.String(100), nullable=False)  # Unique identifier for the user
    query = db.Column(db.Text, nullable=False)  # User's question
    response = db.Column(db.Text, nullable=False)  # Chatbot's reply
    timestamp = db.Column(db.DateTime, default=lambda: datetime.datetime.utcnow())  # Auto timestamp

    def __repr__(self):
        return f"<ChatRecord {self.id} - {self.user_id}>"
