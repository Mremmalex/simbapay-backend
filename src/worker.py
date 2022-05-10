from flask import Flask, jsonify, make_response
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

from flask_sqlalchemy import SQLAlchemy


load_dotenv()

app = Flask(__name__)


database_name = os.environ["DATABASE_NAME"]
database_user = os.environ["DATABASE_USER"]
database_password = os.environ["DATABASE_PASSWORD"]

app.config['SECRET_KEY'] = "thisisasecurekey"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{database_user}:{database_password}:@localhost/{database_name}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db = SQLAlchemy(app)
migrate = Migrate(app, db)


from src.user.userController import route
app.register_blueprint(route)


@app.get("/")
def home():
    return make_response(jsonify({'res': "user register"}))
