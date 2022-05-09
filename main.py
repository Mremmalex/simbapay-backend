from flask import Flask, jsonify
from flask_migrate import Migrate
from src.user.userController import user
from src.utils.db import db
import os


app = Flask(__name__)
dbname = os.environ["DATABASE_NAME"]
app.config['SECRET_KEY'] = "thisisasecurekey"
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://root:root:5432/{dbname}"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)
migrate = Migrate(app, db)


@app.get("/")
def home():
    return jsonify({"message": "welcome to simba pay"})


app.register_blueprint(user)

if __name__ == "__main__":
    app.run(debug=True)
