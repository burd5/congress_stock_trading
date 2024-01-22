import pytest
from api.lib.db import drop_all_tables, save, get_db, close_db
from settings import TEST_DB, USER, PASSWORD
from api.models import Stock, Politician, Trade
from api import create_app
import json

@pytest.fixture(scope='module')
def app():
    flask_app = create_app(dbname=TEST_DB, user=USER, password=PASSWORD)

    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(conn, cursor)
        build_records(conn, cursor)

        conn.commit()
        close_db()
    yield flask_app

    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(conn, cursor)
        close_db()

def build_records(conn, cursor):
    stock_markers = ['', 'AAPL', 'MSFT', 'T', 'NVDA', 'PLTR', 'PYPL', 'NFLX', 'GOOG']
    stock_names = ['', 'Apple', 'Microsoft', 'AT&T', 'Nvidia', 'Palintir', 'Paypal', 'Netflix', 'Google']
    politicians = ['', 'Elizabeth Warren', 'Donald Trump', 'Nancy Pelosi', 'Ron DeSantis', 'Bernie Sanders', 'Tim Scott', 'Corey Booker', 'Ted Cruz']
    for i in range(1, 9):
        stock = Stock(id= i, stock_marker = stock_markers[i], company_name = stock_names[i])
        save(stock, conn, cursor)
        politician = Politician(id = i, name = politicians[i])
        save(politician, conn, cursor)
        trade = Trade(politician_id = politician.id, stock_id = stock.id)
        save(trade, conn, cursor)
        

@pytest.fixture()
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_home_route(client):
    response = client.get('/')
    assert b'Welcome to the Congress Trades API' in response.data

def test_politicians_route_shows_all_politicians(client):
    response = client.get('/politicians')
    politicians = json.loads(response.data)
    assert len(politicians) == 8
    assert politicians[0]['name'] == 'Elizabeth Warren'
    assert politicians[-1]['name'] == 'Ted Cruz'

def test_politician_trades_id_shows_all_trades_from_politician(client):
    response = client.get('/politicians/trades/2')
    politician = json.loads(response.data)
    assert politician[0]['politician'] == 'Donald Trump'
    assert politician[0]['stock'] == 'MSFT'

def test_trade_route_shows_all_trades(client):
    response = client.get('/trades')
    trades = json.loads(response.data)
    assert len(trades) == 8

def test_trades_marker_shows_all_trades_for_that_stock(client):
    response = client.get('/trades/PYPL')
    trades = json.loads(response.data)
    assert len(trades) == 1

def test_stocks_politicians_marker_shows_politicians_who_bought_stock(client):
    response = client.get('/stocks/politicians/AAPL')
    politicians = json.loads(response.data)
    assert len(politicians) == 1