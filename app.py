from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import Configuration
from database import db
from models import User, Investment, UserPortfolio, FAQ, Testimonial
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Configuration)

db.init_app(app)
migrate = Migrate(app, db)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    faqs = FAQ.query.all()
    testimonials = Testimonial.query.all()
    investments = Investment.query.all()
    return render_template('index.html', current_user=current_user, faqs=faqs, testimonials=testimonials, investments=investments)

@app.route('/list_investments')
@login_required
def list_investments():
    investments = Investment.query.all()
    return render_template('list_investments.html', investments=investments)

@app.route('/add_investment', methods=['GET', 'POST'])
@login_required
def add_investment():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        date = request.form['date']

        new_investment = Investment(name=name, amount=amount, date=date, user_id=current_user.id)

        db.session.add(new_investment)
        db.session.commit()
        return redirect(url_for('list_investments'))

    return render_template('add_investment.html')

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        confirm_password = request.form['confirm_password']

        if not email or not password or not username:
            return render_template('signup.html', error='All fields are required.')

        if password != confirm_password:
            return render_template('signup.html', error='Passwords do not match')

        user = User.query.filter_by(email=email).first()
        if user:
            return render_template('signup.html', error='Email already exists')

        hashed_password = generate_password_hash(password)
        user = User(username=username, email=email, password_hash=hashed_password)

        db.session.add(user)
        db.session.commit()

        return render_template('login.html', message='Sign up successful! Please log in.')

    return render_template('signup.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        print(f"Email: {email}, Password: {password}")  # Debug print
        
        user = User.query.filter_by(email=email).first()
        print(f"User found: {user is not None}")  # Debug print

        if user and user.check_password(password):
            print("Logging in user")  # Debug print
            login_user(user)
            return redirect(url_for('index'))
        else:
            return render_template('login.html', error='Invalid email or password')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)





