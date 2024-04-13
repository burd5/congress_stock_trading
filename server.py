from backend.api import create_app, db
from flask import jsonify, request
from backend.api.models import Trade, Stock, Politician
from backend.api.lib.db import to_dict
from flask_cors import CORS


app = create_app()
CORS(app)


@app.route('/')
def home():
    return 'Welcome to the Congress Trades API'

@app.route('/politicians/<id>')
def politicians(id):
    politician = Politician.politician(id)
    return jsonify(politician)

# @app.route('/politicians/<id>')
# def politician(id):
#     politician = db.session.query(Politician).filter_by(id=id)
#     return jsonify([to_dict(politician) for politician in politicians])

@app.route('/politicians/trades/<id>')
def politician_trades(id):
    trades = db.session.query(Trade).filter_by(politician_id=id)
    return jsonify([to_dict(trade) for trade in trades])

@app.route('/trades')
def trades():
    trades = Trade.trades()
    return jsonify(trades)


@app.route('/trades/<marker>')
def trades_by_stock(marker):
    stock = db.session.query(Stock).filter_by(stock_marker=marker.upper()).first()
    return jsonify([to_dict(trade) for trade in stock.trades]) if stock else []
  

@app.route('/stock-info')
def politicians_who_bought_stock():
    # stock = db.session.query(Stock).filter_by(stock_marker=marker.upper()).first()
    # return jsonify([to_dict(politician) for politician in stock.politicians]) if stock else []
    ticker = request.args.get('ticker')
    date = request.args.get('date')
    decoded_date = '-'.join(date.split('%2F'))
    month, day, year = decoded_date.split('-')
    stock_data = Stock().find_stock_history(ticker, f'{year}-{month}-{day}')
    return jsonify(stock_data)

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'Politician': Politician, 'Trade': Trade, 'Stock': Stock}