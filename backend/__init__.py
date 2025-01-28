from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_cors import CORS

# Initialize extensions
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuration
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///faq_assistant.db"
    app.config['SESSION_TYPE'] = 'filesystem'

    # Initialize extensions with the app
    db.init_app(app)
    Session(app)
    CORS(app)

    return app
