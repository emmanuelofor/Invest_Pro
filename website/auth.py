from flask import Blueprint, flash, render_template, request, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_required, login_user, logout_user, current_user
from .models import User
from website import db

auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = User.query.filter_by(email=username).first()

        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully.')
                login_user(user, remember=True)
                return redirect(url_for('views.homepage'))
            else:
                flash('Invalid email or password')
                return render_template('auth.login')
        else:
            flash('User Does Not Exist, Try Again')
            return render_template('login.html')

    return render_template('login.html', user=current_user)


@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        first_name = request.form.get('first_name')  # Updated field name
        last_name = request.form.get('last_name')    # Updated field name
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')

        # Check if email is None or empty
        if email is None or email.strip() == '':
            flash('Email is required', 'danger')
        elif len(email) < 6:
            flash('Email must be at least 6 characters', 'danger')
        # Check if first_name and last_name are None or empty
        elif first_name is None or first_name.strip() == '':
            flash('First Name is required', 'danger')
        elif last_name is None or last_name.strip() == '':
            flash('Last Name is required', 'danger')
        elif not username:
            flash('Username is required', 'danger')
        elif len(username) < 4:
            flash('Username must be at least 4 characters', 'danger')
        elif not password:
            flash('Password is required', 'danger')
        elif password != confirm_password:
            flash('Passwords do not match', 'danger')
        else:
            # Check if the email already exists in the database
            user = User.query.filter_by(email=email).first()
            if user:
                flash('User already exists', 'danger')
            else:
                new_user = User(
                    email=email,
                    username=username,
                    first_name=first_name,  # Store first_name in the User model
                    last_name=last_name,    # Store last_name in the User model
                    password=generate_password_hash(password, method='sha256')
                )
                db.session.add(new_user)
                db.session.commit()
                # Flash a success message
                flash('Account created successfully', 'success')
                login_user(new_user, remember=True)
                return redirect(url_for('views.homepage'))

    return render_template('signup.html', user=current_user)


@auth.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    global user
    user = None
    return redirect('/')
