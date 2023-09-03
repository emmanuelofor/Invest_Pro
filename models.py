from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class Investment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), index=True)
    type = db.Column(db.String(64))
    description = db.Column(db.String(256))
    risk_level = db.Column(db.String(64))

class UserPortfolio(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    investment_id = db.Column(db.Integer, db.ForeignKey('investment.id'))
    amount = db.Column(db.Float)

class Resource(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(64))
    content = db.Column(db.String(256))
    link = db.Column(db.String(128))