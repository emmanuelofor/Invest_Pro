# Import required modules
from flask import Flask, render_template, request, redirect, url_for, abort
from flask_login import LoginManager, login_user, current_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from config import Configuration
from database import db
from models import User, Investment, UserPortfolio, FAQ, Testimonial, Opportunity, Contact
from flask_migrate import Migrate

# Initialize Flask app and configurations
app = Flask(__name__)
app.config.from_object(Configuration)

# Initialize database and migration
db.init_app(app)
migrate = Migrate(app, db)

# Initialize login manager
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Load user for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Home route
@app.route('/')
def index():
    faqs = FAQ.query.all()
    testimonials = Testimonial.query.all()
    investments = Investment.query.all()
    return render_template('index.html', current_user=current_user, faqs=faqs, testimonials=testimonials, investments=investments)

# List investments route
@app.route('/list_investments')
# @login_required
def list_investments():
    # investments = Investment.query.all()
    # return render_template('list_investments.html', investments=investments)
    return render_template('list_investments.html')

# Add investment route
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

# Portfolio tracking route
@app.route('/portfolio_tracking')
@login_required
def portfolio_tracking():
    user_portfolios = UserPortfolio.query.filter_by(user_id=current_user.id).all()
    return render_template('portfolio_tracking.html', portfolios=user_portfolios)

# Opportunities route
@app.route('/opportunities')
def opportunities():
    # opportunities = Opportunity.query.all()
    # return render_template('opportunities.html', opportunities=opportunities)
    return render_template('opportunities.html')

# Contact route
@app.route('/contact')
def contact():
    # contacts = Contact.query.all()
    # return render_template('contact.html', contacts=contacts)
    return render_template('contact.html')


# Submit contact route
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        new_contact = Contact(name=name, email=email, subject=subject, message=message)

        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('contact'))

    return redirect(url_for('contact'))

# Signup route
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

# Login route
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

# Logout route
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

# Run the application
if __name__ == '__main__':
    app.run(debug=True)





