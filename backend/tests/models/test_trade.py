import pytest
from api.lib.db import drop_all_tables, test_conn, test_cursor, save
import api.models as models
import datetime

@pytest.fixture()
def build_trades():
    drop_all_tables(test_conn, test_cursor)
    aapl_stock = save(models.Stock(id = 1, stock_marker = 'AAPL', company_name = 'Apple'), test_conn, test_cursor)
    pelosi = save(models.Politician(id = 1, name = 'Nancy Pelosi', political_party = 'Democrat'), test_conn, test_cursor)
    trade = save(models.Trade(id = 1, stock_id = aapl_stock.id, politician_id = pelosi.id, transaction_date = '2022-12-31', amount = '$15,001 - $50,000', purchased_or_sold = 'Purchased'), test_conn, test_cursor)
    yield trade
    drop_all_tables(test_conn, test_cursor)


def test_build_instance(build_trades):
    assert (isinstance(build_trades, models.Trade))

def test_stock(build_trades):
    stock = build_trades.stock(test_cursor)
    assert stock.id == 1
    assert stock.stock_marker == 'AAPL'

def test_politician(build_trades):
    politician = build_trades.politician(test_cursor)
    assert politician.name == 'Nancy Pelosi'
    assert politician.political_party == 'Democrat'

def test_to_json(build_trades):
    json_response = build_trades.to_json(test_cursor)
    assert json_response['stock'] == 'AAPL'
    assert json_response['transaction_date'].strftime('%Y-%m-%d') == '2022-12-31'
    assert json_response['purchased_or_sold'] == 'Purchased'