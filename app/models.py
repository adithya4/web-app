from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()
class Users(db.Model):
    __tablename__ = "Users"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), nullable=False, unique=True)
    password = db.Column(db.String(256), nullable=False)
    image = db.Column(db.LargeBinary, nullable=True)
    time = db.Column(db.DateTime, default=datetime.now())
    #foreign key
    posts = db.relationship("Posts", backref="author", lazy=True)

class Posts(db.Model):
    __tablename__ = "Posts"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(256), nullable=False)
    time = db.Column(db.DateTime, default=datetime.now())
    
    username = db.Column(db.String(64),db.ForeignKey("Users.username"), nullable=False)