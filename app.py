import os
from dotenv import load_dotenv
from flask import Flask
from flask_restful import Api
from flask_session import Session
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta
from flask_jwt_extended import get_jwt_identity, jwt_required, JWTManager

from lib import db, User, Message, Profile, Property
from config import Config 
from extensions import mail

# Load environment variables from .env file
load_dotenv()

def create_app():
    # Initialize the Flask application
    app = Flask(__name__)

    # Configure the app with using config class
    app.config.from_object(Config)
    # Initialize extensions
    jwt = JWTManager(app)
    CORS(app)
    migrate = Migrate(app, db)
    Session(app)
    db.init_app(app)
    api = Api(app)
    mail.init_app(app)

    # JWT configuration
    @jwt.user_identity_loader
    def user_identity_lookup(user):
        return user.id
    
    @jwt.user_lookup_loader
    def user_lookup_callback(_jwt_header, jwt_data):
        identity = jwt_data["sub"]
        return User.query.filter_by(id=identity).one_or_none()

    # Import routes
    from routes import (
        Index, Properties, PropertyByID, Roles, 
        UsersByRole, Login, Logout, Whoami, RoomMates, RoommateByID, 
        PropertyForSale, Profiles, ProfileByID, FollowUser, UnfollowUser, 
        SendMessage, Activation, users_bp
    )
    
    # Add resources
    api.add_resource(Index, "/")
    # api.add_resource(Users, '/users', resource_class_args=(mail,))
    # api.add_resource(UserByID, "/users/<int:id>")
    api.add_resource(Properties, "/properties")
    api.add_resource(PropertyByID, "/properties/<int:id>")
    api.add_resource(Roles, "/roles")
    api.add_resource(UsersByRole, "/users/roles/<int:roleId>")
    api.add_resource(Login, "/login")
    api.add_resource(Logout, "/logout")
    api.add_resource(Whoami, "/whoami")
    api.add_resource(RoomMates, "/roommates")
    api.add_resource(RoommateByID, "/roommates/<int:id>")
    api.add_resource(PropertyForSale, "/for-sale")
    api.add_resource(Profiles, "/profiles")
    api.add_resource(ProfileByID, "/profiles/<int:id>")
    api.add_resource(FollowUser, "/follow/<int:user_id>")
    api.add_resource(UnfollowUser, "/unfollow/<int:user_id>")
    api.add_resource(SendMessage, "/send-message")
    api.add_resource(Activation, "/activate")

    app.register_blueprint(users_bp)

    return app

# Create the app and mail instances
app= create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5555)
