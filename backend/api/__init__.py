from flask import Flask, jsonify
from settings import DATABASE, USER, PASSWORD
import psycopg2
import api.models as models
from api.lib.db import find_all


def create_app():
    app = Flask(__name__)

    app.config.from_mapping(
        DB_NAME = DATABASE,
        DB_USER = USER,
        DB_PASSWORD = PASSWORD
    )

    conn = psycopg2.connect(dbname=app.config['DB_NAME'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'])

    app.json.sort_keys = False

    @app.route('/')
    def home():
        return 'Welcome to the Congress Trades API'
    
    @app.route('/politicians')
    def politicians():
        politicians = find_all(models.Politician)
        return jsonify([politician.__dict__ for politician in politicians])
    

    return app