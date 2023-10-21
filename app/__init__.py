from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/recipes.db'
app.config['SECRET_KEY'] = 'your_secret_key'

db = SQLAlchemy(app)
