import flask_login as login
from flask_login import current_user

from app.models import db
from app.models.user import User


class AuthManager:
    def __init__(self):
        pass

    @staticmethod
    def init_login(app):
        from flask import request, url_for, redirect
        login_manager = login.LoginManager()
        login_manager.init_app(app)

        # Create user loader function
        @login_manager.user_loader
        def load_user(user_id):
            return db.session.query(User).get(user_id)

        @login_manager.unauthorized_handler
        def unauthorized():
            return redirect(url_for('admin.login_view', next=request.url))

    @staticmethod
    def is_verified_user():
        return current_user.is_verified

    @staticmethod
    def is_accessible():
        return current_user.is_authenticated

    @staticmethod
    def check_auth_admin(username, password):
        # This function is called to check for proper authentication & admin rights
        if username and password:
            user = User.query.filter_by(_email=username).first()
            if user and user.is_correct_password(password) and user.is_admin:
                return True
        return False
