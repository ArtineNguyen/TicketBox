from flask_login import UserMixin, LoginManager, login_user, current_user
from src import db
from flask_wtf import FlaskForm
from wtforms import Form, StringField, PasswordField, SubmitField, validators
from werkzeug.security import generate_password_hash, check_password_hash


class User(UserMixin, db.Model):
    __tablename__ ='users'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True)
    admin = db.Column(db.Boolean, default=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    def check_user(self):
        return User.query.filter_by(email=self.email).first()


class LoginForm(FlaskForm):
    email = StringField('Email')
    password = PasswordField('Password')
    submit = SubmitField('Submit')

class EmailForm(Form):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])

class PasswordForm(Form):
    password = PasswordField('Password', validators=[validators.DataRequired()])
    confirm = PasswordField('Repeat Password', validators=[validators.EqualTo(password, message='Passwords must match.')])

class Oder(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)

class OderItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    oder_id = db.Column(db.Integer)

class Event(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)

class Ticket(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    quanity = db.Column(db.Integer)

class Rating(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    stars = db.Column(db.Integer)
    body = db.Column(db.Text)