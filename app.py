import os
from dotenv import load_dotenv
from flask import Flask, request
from flask_restful import Api, Resource
from flask_session import Session
from flask_cors import CORS

from lib.models import db

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

# init session
Session(app)

# init database
db.init_app(app)

# init api
api = Api(app)

# home route
class Index(Resource):
    
    def get(self):
        return "Welcome to Qeja API"
    
api.add_resource(Index, "/")



if __name__ == '__main__':
    app.run(debug=True, port=5555)