from flask import Flask, request, jsonify, render_template, redirect
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_migrate import Migrate
from models import db, Investment, UserPortfolio, Resource, User  
from werkzeug.security import generate_password_hash, check_password_hash
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
        email = request.form.get('email')
        user = User.query.filter_by(email=email).first()
        
        if user:
            # Generate a token
            token = s.dumps(email, salt='reset-password')
            
            # Send an email
            msg = Message('Password Reset Request', sender='noreply@investpro.com', recipients=[email])
            msg.body = f'Reset your password by clicking this link: http://127.0.0.1:5000/reset_password/{token}'
            mail.send(msg)
            
            return 'An email for password reset has been sent.'
        
        else:
            return 'Email not found.'
        
    return render_template('reset_password_request.html')


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = s.loads(token, salt='reset-password', max_age=3600)
    except:
        return 'The reset password link is invalid or has expired.'
    
    user = User.query.filter_by(email=email).first()
    
    if request.method == 'POST' and user:
        new_password = request.form.get('new_password')
        user.set_password(new_password)
        db.session.commit()
        
        return 'Password has been updated!'
        
    return render_template('reset_password.html')


# New route for login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    return render_template('login.html')

# New route for logout
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

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

