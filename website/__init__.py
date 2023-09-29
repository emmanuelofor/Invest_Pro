from os import path
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = 'investpro.db'


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'your_secret_key_here'
    # Use the DB_NAME variable here
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Investment, UserPortfolio, Opportunity, Contact, FAQ, Testimonial

    # Initialize Flask-Login
    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    # Create the database if it doesn't exist
    create_database(app)

    return app


def create_database(app):
    if not path.exists('website/' + DB_NAME):
        try:
            with app.app_context():
                db.create_all()
                print('Created database!')
        except Exception as e:
            print(f"Error creating database: {e}")


if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)
