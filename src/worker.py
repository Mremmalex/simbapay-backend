from flask import Flask, jsonify, make_response
from flask_cors import CORS
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_sqlalchemy import SQLAlchemy
from jsonschema import ValidationError

load_dotenv()

app = Flask(__name__)
cors = CORS(app)


database_name = os.environ["DATABASE_NAME"]
database_user = os.environ["DATABASE_USER"]
database_password = os.environ["DATABASE_PASSWORD"]

app.config['SECRET_KEY'] = os.environ['SECRET_KEY']
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_user}:{database_password}:@localhost/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['CORS_HEADERS'] = "Content-Type"

db = SQLAlchemy(app)
migrate = Migrate(app, db)


@app.errorhandler(400)
def bad_request(error):
    if isinstance(error.description, ValidationError):
        original_error = error.description
        return make_response(jsonify({'error': f"{original_error.path[0]} is too short"}), 400)
    # handle other "Bad Request"-errors
    return error


from src.user.userController import route as user
from src.accounts.accountController import route as account
app.register_blueprint(user)
app.register_blueprint(account)


@app.get("/")
def home():
    return make_response(jsonify({'res': "user register"}))
