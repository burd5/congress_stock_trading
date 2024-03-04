from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from settings import DATABASE, USER, PASSWORD

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    conn_str = f"postgresql://{USER}@localhost:5432/{DATABASE}"
    app.json.sort_keys = False
    app.config['SQLALCHEMY_DATABASE_URI'] = conn_str
    db.init_app(app)
    return app