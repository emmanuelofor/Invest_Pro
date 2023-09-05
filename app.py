from flask import Flask, request, jsonify, render_template, redirect, flash, url_for
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from models import db, Investment, UserPortfolio, Resource, User  
from flask_mail import Mail, Message
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

# Database Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///investpro.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'your-secret-key'

db.init_app(app)  # Initialize the database
migrate = Migrate(app, db)  # Apply Migrations

# Initialize Flask-Mail
mail = Mail(app)
app.config['MAIL_SERVER'] = 'smtp.your-email-provider.com'
app.config['MAIL_USERNAME'] = 'your-email@example.com'
app.config['MAIL_PASSWORD'] = 'your-email-password'

# Serializer for generating random tokens
s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Create the user
        user = User(username=username, email=email)
        user.set_password(password)
        
        # Commit the user to the database
        db.session.add(user)
        db.session.commit()

        # Generate token and send email for email confirmation
        token = s.dumps(email, salt='email-confirm')
        msg = Message('Confirm Email', sender='noreply@investpro.com', recipients=[email])
        msg.body = f'Click here to confirm your email: http://127.0.0.1:5000/confirm_email/{token}'
        mail.send(msg)

        return 'Signup successful! Please check your email to confirm.'
    return render_template('signup.html')

@app.route('/confirm_email/<token>')
def confirm_email(token):
    try:
        email = s.loads(token, salt='email-confirm', max_age=3600)
    except:
        return 'The confirmation link is invalid or has expired.'

    user = User.query.filter_by(email=email).first()
    if user:
        user.email_confirmed = True
        db.session.commit()
    return 'Email confirmed!'

@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if request.method == 'POST':
        email = request.form['email']
        user = User.query.filter_by(email=email).first()
        if user:
            token = s.dumps(user.email, salt='email-confirm-key')
            msg = Message('Reset Password', sender='noreply@example.com', recipients=[user.email])
            msg.body = f"Click here to reset your password: {url_for('reset_password', token=token, _external=True)}"
            mail.send(msg)
            flash('Check your email for the instructions to reset your password')
    return render_template('reset_password_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='email-confirm-key', max_age=86400)
    except:
        flash('The reset link is invalid or has expired.')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']

        if new_password == confirm_password:
            user = User.query.filter_by(email=email).first()
            user.password_hash = generate_password_hash(new_password)
            db.session.commit()
            flash('Your password has been updated!')
            return redirect(url_for('login'))
        else:
            flash('Passwords do not match.')
    return render_template('reset_password.html')


# New route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            return redirect(url_for('index'))
        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


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

