import os
from sqlalchemy import create_engine
from flask import Flask
from app.models import db
from app.views.auth import auth_bp
from app.views.posts import post_bp
from datetime import timedelta
from dotenv import load_dotenv

load_dotenv()

def create_app():
    app = Flask(__name__)
    app.secret_key = os.getenv("SECRET_KEY")
    app.permanent_session_lifetime = timedelta(minutes=5)
    app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DB_URL")
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.init_app(app)

    with app.app_context():
        db.create_all()
        print("Database created successfully")

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)

    return app