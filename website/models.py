# Import required modules
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import check_password_hash
from . import db


from sqlalchemy.sql import func


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))
    username = db.Column(db.String(150))
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    date_of_birth = db.Column(db.Date, default=datetime.utcnow)

    def check_password(self, password):
        # Checking the hashed password
        return check_password_hash(self.password_hash, password)


# Investment model for storing investment information
class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64))
    description = db.Column(db.String(256))
    risk_level = db.Column(db.String(64))
    amount = db.Column(db.Float)
    date = db.Column(db.Date)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))


# UserPortfolio model for linking users and their investments
class UserPortfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    investment_id = db.Column(db.Integer, db.ForeignKey('investment.id'))
    amount = db.Column(db.Float)


# Opportunity model for storing potential investment opportunities
class Opportunity(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    description = db.Column(db.String(256))
    type = db.Column(db.String(64))
    expected_return = db.Column(db.Float)
    risk_level = db.Column(db.String(64))


# Contact model for storing contact inquiries
class Contact(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    message = db.Column(db.String(1000), nullable=False)


# FAQ model for storing frequently asked questions and answers
class FAQ(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(500), nullable=False)
    answer = db.Column(db.String(1000), nullable=False)


# Testimonial model for storing user testimonials
class Testimonial(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(1000), nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
