from flask import Flask, request, jsonify, render_template, redirect
from flask_migrate import Migrate
from models import db, Investment, UserPortfolio, Resource  # Import db and models

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///investpro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)  # Initialize the database
migrate = Migrate(app, db)  # Apply Migrations

@app.route('/')
def home():
    return "Welcome to InvestPro!"

@app.route('/add_investment', methods=['GET', 'POST'])
def add_investment():
    if request.method == 'POST':
        name = request.form.get('name')
        type = request.form.get('type')
        description = request.form.get('description')
        risk_level = request.form.get('risk_level')

        new_investment = Investment(name=name, type=type, description=description, risk_level=risk_level)
        db.session.add(new_investment)
        db.session.commit()

        return redirect('/list_investments')

    return render_template('add_investment.html')

@app.route('/list_investments', methods=['GET'])
def list_investments():
    investments = Investment.query.all()
    return render_template('list_investments.html', investments=investments)

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
