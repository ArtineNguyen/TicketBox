from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, LoginManager, login_required, login_user, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import enum
from flask_moment import Moment


app = Flask(__name__, static_folder="src/static")
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'My secret'

moment = Moment ()
moment.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'
db = SQLAlchemy(app)
# migrate = migrate(app,db)

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    avatar_url = db.Column(db.Text)

    def generate_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


# class Post(db.Model):
#     __tablename__ = 'posts'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(
#         db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
#     image_url = db.Column(db.Text)
#     view_count = db.Column(db.Integer, default=0)


# class Comment(db.Model):
#     __tablename__ = 'comments'
#     id = db.Column(db.Integer, primary_key=True)
#     body = db.Column(db.String, nullable=False)
#     user_id = db.Column(db.Integer, nullable=False)
#     post_id = db.Column(db.Integer, nullable=False)
#     created_at = db.Column(db.DateTime, server_default=db.func.now())
#     updated_at = db.Column(
#         db.DateTime, server_default=db.func.now(), server_onupdate=db.func.now())
#     image_url = db.Column(db.Text)

