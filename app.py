import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api
from flask_session import Session
from flask_cors import CORS
from flask_migrate import Migrate
from datetime import timedelta

from flask_jwt_extended import get_jwt_identity
from flask_jwt_extended import jwt_required
from flask_jwt_extended import JWTManager

from lib import db, User, Profile, Property, Role, Message, Post, followers

from routes import Index, Users, UserByID, Properties, PropertyByID, Roles, UsersByRole, Login, Logout, Whoami, RoomMates, RoommateByID, PropertyForSale, ViewPosts, PostByID, Follow

# Load env variables
load_dotenv()

# init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(minutes=30)
jwt = JWTManager(app)

# init cors
CORS(app, supports_credentials=True)

# init migration
migrate = Migrate(app, db)

# init session
Session(app)

# init database
db.init_app(app)

# init api
api = Api(app)

# Register a callback function that takes whatever object is passed in as the
# identity when creating JWTs and converts it to a JSON serializable format.
@jwt.user_identity_loader
def user_identity_lookup(user):
    return user.id


# Register a callback function that loads a user from your database whenever
# a protected route is accessed. This should return any python object on a
# successful lookup, or None if the lookup failed for any reason (for example
# if the user has been deleted from the database).
@jwt.user_lookup_loader
def user_lookup_callback(_jwt_header, jwt_data):
    identity = jwt_data["sub"]
    return User.query.filter_by(id=identity).one_or_none()


# Routes
api.add_resource(Index, "/") # Home Route
api.add_resource(Users, "/users") # Users Route
api.add_resource(UserByID, "/users/<int:id>") # Users By ID Route
api.add_resource(Properties, "/properties") # Properties Route
api.add_resource(PropertyByID, "/properties/<int:id>") # Property By ID Route
api.add_resource(Roles, "/roles") # Roles Route
api.add_resource(UsersByRole, "/users/roles/<int:roleId>") # Users By Role ID Route
api.add_resource(Login, "/login") # Login Route
api.add_resource(Logout, "/logout") # Logout Route
api.add_resource(Whoami, "/whoami") # Protected Route (Check if a user exists)
api.add_resource(RoomMates, "/roommates") # Room mates Route
api.add_resource(RoommateByID, "/roommates/<int:id>") # Room mate By ID Route
api.add_resource(PropertyForSale, "/for-sale") # Properties For Sale Route
api.add_resource(ViewPosts, "/posts") # All Posts Route
api.add_resource(PostByID, "/posts/<int:id>") # All Posts Route
api.add_resource(Follow, "/follow/<int:user_id>") # Following a user Route



if __name__ == '__main__':
    app.run(debug=True, port=5555)