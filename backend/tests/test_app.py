import pytest
from api.lib.db import drop_all_tables, test_conn, test_cursor, save, get_db, close_db
from settings import TEST_DB, USER, PASSWORD
import api.models as models
from api import create_app

@pytest.fixture(scope='module')
def app():
    flask_app = create_app(db_name=TEST_DB, user=USER, password=PASSWORD)

    with flask_app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(test_conn, test_cursor)
        build_records(conn, cursor)

        conn.commit()
        close_db()
    yield flask_app

    with flask_app.app_context():
        close_db()
        conn = get_db()
        cursor = conn.cursor()
        drop_all_tables(test_conn, test_cursor)
        close_db()

def build_records(test_conn, test_cursor):
    pass


@pytest.fixture()
def client(app):
    return app.test_client()

def test_home_route():
    pass

def test_politicians_route_shows_all_politicians():
    pass

def test_politician_trades_id_shows_all_trades_from_politician():
    pass

def test_trade_route_shows_all_trades():
    pass

def test_trades_marker_shows_all_trades_for_that_stock():
    pass

def test_stocks_politicians_marker_shows_politicians_who_bought_stock():
    pass