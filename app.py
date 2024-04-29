import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api
from flask_session import Session
from flask_cors import CORS
from flask_migrate import Migrate

from lib import db, User, Profile, Property, Role, Message

from routes import Index, Users, UserByID, Properties, PropertyByID, Roles, UsersByRole, Login, Logout

# Load env variables
load_dotenv()

# init app
app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

app.config["SECRET_KEY"] = os.getenv("APP_SECRET_KEY")
app.config["SESSION_TYPE"] = "filesystem"

# init cors
CORS(app)

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



if __name__ == '__main__':
    app.run(debug=True, port=5555)