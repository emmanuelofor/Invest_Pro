from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///investpro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
migrate = Migrate(app, db)

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

@app.route('/')
def home():
    return "Welcome to InvestPro!"

@app.route('/add_investment', methods=['POST'])
def add_investment():
    name = request.json.get('name')
    type = request.json.get('type')
    description = request.json.get('description')
    risk_level = request.json.get('risk_level')

    new_investment = Investment(name=name, type=type, description=description, risk_level=risk_level)
    db.session.add(new_investment)
    db.session.commit()

    return jsonify({"message": "Investment added", "investment_id": new_investment.id})

@app.route('/list_investments', methods=['GET'])
def list_investments():
    investments = Investment.query.all()
    investments_list = [{"name": i.name, "type": i.type, "description": i.description, "risk_level": i.risk_level} for i in investments]
    return jsonify(investments_list)

@app.route('/add_portfolio', methods=['POST'])
def add_portfolio():
    investment_id = request.json.get('investment_id')
    amount = request.json.get('amount')

    new_portfolio = UserPortfolio(investment_id=investment_id, amount=amount)
    db.session.add(new_portfolio)
    db.session.commit()

    return jsonify({"message": "Portfolio entry added", "portfolio_id": new_portfolio.id})

@app.route('/list_portfolios', methods=['GET'])
def list_portfolios():
    portfolios = UserPortfolio.query.all()
    portfolios_list = [{"investment_id": p.investment_id, "amount": p.amount} for p in portfolios]
    return jsonify(portfolios_list)

@app.route('/add_resource', methods=['POST'])
def add_resource():
    title = request.json.get('title')
    content = request.json.get('content')
    link = request.json.get('link')

    new_resource = Resource(title=title, content=content, link=link)
    db.session.add(new_resource)
    db.session.commit()

    return jsonify({"message": "Resource added", "resource_id": new_resource.id})

@app.route('/list_resources', methods=['GET'])
def list_resources():
    resources = Resource.query.all()
    resources_list = [{"title": r.title, "content": r.content, "link": r.link} for r in resources]
    return jsonify(resources_list)

if __name__ == '__main__':
    app.run(debug=True)