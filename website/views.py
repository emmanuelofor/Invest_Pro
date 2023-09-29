from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user, login_user, logout_user
from .models import FAQ, Contact, Investment, Testimonial, User, UserPortfolio
from . import db

views = Blueprint('views', __name__)

# Home route


@views.route('/')
def index():
    faqs = FAQ.query.all()
    testimonials = Testimonial.query.all()
    investments = Investment.query.all()
    return render_template('index.html', current_user=current_user, faqs=faqs, testimonials=testimonials, investments=investments)

# List investments route


@views.route('/homepage')
@login_required
def homepage():
    return render_template('homepage.html')


@views.route('/list_investments')
# @login_required
def list_investments():
    # investments = Investment.query.all()
    # return render_template('list_investments.html', investments=investments)
    return render_template('list_investments.html')

# Add investment route


@views.route('/add_investment', methods=['GET', 'POST'])
@login_required
def add_investment():
    if request.method == 'POST':
        name = request.form['name']
        amount = float(request.form['amount'])
        date = request.form['date']

        new_investment = Investment(
            name=name, amount=amount, date=date, user_id=current_user.id)

        db.session.add(new_investment)
        db.session.commit()
        return redirect(url_for('list_investments'))

    return render_template('add_investment.html')

# Portfolio tracking route


@views.route('/portfolio_tracking')
@login_required
def portfolio_tracking():
    user_portfolios = UserPortfolio.query.filter_by(
        user_id=current_user.id).all()
    return render_template('portfolio_tracking.html', portfolios=user_portfolios)

# Opportunities route


@views.route('/opportunities')
def opportunities():
    # opportunities = Opportunity.query.all()
    # return render_template('opportunities.html', opportunities=opportunities)
    return render_template('opportunities.html')


# Contact route
@views.route('/contact')
def contact():
    # contacts = Contact.query.all()
    # return render_template('contact.html', contacts=contacts)
    return render_template('contact.html')


# Submit contact route
@views.route('/submit_contact', methods=['POST'])
def submit_contact():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        subject = request.form['subject']
        message = request.form['message']

        new_contact = Contact(name=name, email=email,
                              subject=subject, message=message)

        db.session.add(new_contact)
        db.session.commit()

        return redirect(url_for('contact'))

    return redirect(url_for('contact'))

# Signup route


# Logout route


@views.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))
