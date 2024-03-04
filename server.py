from backend.api import create_app, db
from flask import jsonify
from backend.api.models import Trade, Stock, Politician
from backend.api.lib.db import to_dict

app = create_app()

@app.route('/')
def home():
    return 'Welcome to the Congress Trades API'

@app.route('/politicians')
def politicians():
    politicians = db.session.query(Politician).all()
    return jsonify([to_dict(politician) for politician in politicians])

@app.route('/politicians/trades/<id>')
def politician_trades(id):
    trades = db.session.query(Trade).filter_by(politician_id=id)
    return jsonify([to_dict(trade) for trade in trades])

@app.route('/trades')
def trades():
    trades = db.session.query(Trade).all()
    return jsonify([to_dict(trade) for trade in trades])

@app.route('/trades/<marker>')
def trades_by_stock(marker):
    stock = db.session.query(Stock).filter_by(stock_marker=marker.upper()).first()
    return jsonify([to_dict(trade) for trade in stock.trades]) if stock else []
  

@app.route('/stocks/politicians/<marker>')
def politicians_who_bought_stock(marker):
    stock = db.session.query(Stock).filter_by(stock_marker=marker.upper()).first()
    return jsonify([to_dict(politician) for politician in stock.politicians]) if stock else []

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Politician': Politician, 'Trade': Trade, 'Stock': Stock}