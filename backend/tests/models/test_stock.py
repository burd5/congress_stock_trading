import pytest
from api.lib.db import drop_all_tables, test_conn, test_cursor, save
import api.models as models

@pytest.fixture()
def build_stocks():
    drop_all_tables(test_conn, test_cursor)
    msft = save(models.Stock(id = 1, stock_marker = 'MSFT', company_name = 'Microsoft'), test_conn, test_cursor)
    t = save(models.Stock(id = 2, stock_marker = 'T', company_name='AT&T'), test_conn, test_cursor)
    mcconnell = save(models.Politician(id = 1, name = 'Mitch McConnell', political_party = 'Republican', part_of_congress='Senate'), test_conn, test_cursor)
    trade_1 = save(models.Trade(id = 1, stock_id = msft.id, politician_id = mcconnell.id, amount = '$100,000'), test_conn, test_cursor)
    trade_2 = save(models.Trade(id = 2, stock_id = t.id, politician_id = mcconnell.id, amount = '$500,000'), test_conn, test_cursor)
    yield [msft, t, trade_1, trade_2]
    drop_all_tables(test_conn, test_cursor)

def test_create_stock_instance(build_stocks):
    assert isinstance(build_stocks[1], models.Stock)

def test_politicians(build_stocks):
    politician = build_stocks[0].politicians(test_cursor)
    politician_2 = build_stocks[1].politicians(test_cursor)
    assert politician[0].name == 'Mitch McConnell'
    assert politician[0].part_of_congress == 'Senate'
    assert politician_2[0].political_party == 'Republican'

def test_trades(build_stocks):
    msft_trade = build_stocks[0].trades(test_cursor)
    t_trade = build_stocks[1].trades(test_cursor)
    assert msft_trade[0].amount == '$100,000'
    assert t_trade[0].stock_id == 2
    assert len(msft_trade) == 1

def test_find_by_stock_marker(build_stocks):
    stock1 = models.Stock.find_by_stock_marker('T', test_cursor)
    stock2 = models.Stock.find_by_stock_marker('MSFT', test_cursor)
    assert stock1.company_name == 'AT&T'
    assert stock2.company_name == 'Microsoft'

def test_find_by_company_name(build_stocks):
    stock1 = models.Stock.find_by_company_name('Microsoft', test_cursor)
    stock2 = models.Stock.find_by_company_name('AT&T', test_cursor)
    assert stock1[0].stock_marker == 'MSFT'
    assert stock2[0].stock_marker == 'T'