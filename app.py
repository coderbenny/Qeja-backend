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

from lib import db, User, Profile, Property, Role, Message

from routes import Index, Users, UserByID, Properties, PropertyByID, Roles, UsersByRole, Login, Logout, Whoami, RoomMates, RoommateByID, PropertyForSale

# Load env variables
load_dotenv()

# init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_ACCESS_TOKEN_EXPIRES"] = timedelta(hours=1)
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



if __name__ == '__main__':
    app.run(debug=True, port=5555)