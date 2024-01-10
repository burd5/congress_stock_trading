import pytest
from api.lib.db import drop_all_tables, test_conn, test_cursor, save
import api.models as models

@pytest.fixture()
def build_politicians():
    drop_all_tables(test_conn, test_cursor)
    politician1 = save(models.Politician(id = 1, name='Mike Johnson', state='LA', part_of_congress='House', political_party = 'Republican', office='LA4'), test_conn, test_cursor)
    politician2 = save(models.Politician(id = 2, name='Bernard Sanders', state='VT', part_of_congress='Senate', political_party='Independent'), test_conn, test_cursor)
    stock = save(models.Stock(id = 1, stock_marker = 'META', company_name = 'Meta'), test_conn, test_cursor)
    trade = save(models.Trade(id = 1, stock_id = stock.id, politician_id = politician2.id), test_conn, test_cursor)
    yield [politician1, politician2, stock, trade]
    drop_all_tables(test_conn, test_cursor)

def test_create_politician_instance(build_politicians):
    assert isinstance(build_politicians[0], models.Politician)

def test_stocks(build_politicians):
    stocks = build_politicians[1].stocks(test_cursor)
    assert stocks[0].stock_marker == 'META'
    assert len(stocks) == 1

def test_trades(build_politicians):
    trades = build_politicians[1].trades(test_cursor)
    assert trades[0].politician_id == 2
    assert len(trades) == 1

def test_find_by_name_house(build_politicians):
    politician = models.Politician.find_by_name_house('Mike Johnson', test_cursor)
    assert politician.office == 'LA4'
    assert politician.political_party == 'Republican'

def test_find_by_name_senate(build_politicians):
    politician = models.Politician.find_by_name_senate('Bernard Sanders', test_cursor)
    assert politician.political_party == 'Independent'
    assert politician.state == 'VT'

def test_find_by_office(build_politicians):
    politician = models.Politician.find_by_office('LA4', 'Mike Johnson', test_cursor)
    assert politician.state == 'LA'
    assert politician.part_of_congress == 'House'