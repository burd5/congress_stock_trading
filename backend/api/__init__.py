from flask import Flask, jsonify
from settings import DATABASE, USER, PASSWORD
import psycopg2
import backend.api.models as models
from backend.api.lib.orm import find_all, find

def create_app(dbname, user, password):
    app = Flask(__name__)

    app.config.from_mapping(
        DB_NAME = dbname,
        DB_USER = user,
        DB_PASSWORD = password
    )

    conn = psycopg2.connect(dbname=app.config['DB_NAME'], user=app.config['DB_USER'], password=app.config['DB_PASSWORD'])

    app.json.sort_keys = False

    @app.route('/')
    def home():
        return 'Welcome to the Congress Trades API'
    
    @app.route('/politicians')
    def politicians():
        cursor = conn.cursor()
        politicians = find_all(cursor, models.Politician)
        return jsonify([politician.__dict__ for politician in politicians])
    
    @app.route('/politicians/trades/<id>')
    def politician_trades(id):
        cursor = conn.cursor()
        politician = find(cursor, models.Politician, id)
        trades = politician.trades(cursor)
        return jsonify([trade.to_json(cursor) for trade in trades])
    
    @app.route('/trades')
    def trades():
        cursor = conn.cursor()
        trades = find_all(cursor, models.Trade)
        return jsonify([trade.__dict__ for trade in trades])

    @app.route('/trades/<marker>')
    def trades_by_stock(marker):
        cursor = conn.cursor()
        stock = models.Stock.find_by_stock_marker(marker.upper(), cursor)
        trades = stock.trades(cursor)
        return jsonify([trade.to_json(cursor) for trade in trades])
    
    @app.route('/stocks/politicians/<marker>')
    def politicians_who_bought_stock(marker):
        cursor = conn.cursor()
        stock = models.Stock.find_by_stock_marker(marker.upper(), cursor)
        politicians = stock.politicians(cursor)
        return jsonify([politician.__dict__ for politician in politicians])

    return app