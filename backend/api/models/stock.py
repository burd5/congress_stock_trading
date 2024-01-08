import api.models as models
from api.lib.db import build_from_record, build_from_records, cursor
import api.models as models

class Stock(models.BaseClass):
    __table__ = 'stocks'
    attributes = ['id', 'stock_marker', 'company_name']

    def politicians(self):
        cursor.execute(f"""select distinct p.* from politicians p join trades t
                                on p.id = t.politician_id
                                where t.stock_id = %s;""", (self.id,))
        records = cursor.fetchall()
        return build_from_records(models.Politician, records)

    def trades(self):
        cursor.execute(f"""select * from trades
                           where stock_id = %s;""", (self.id,))
        records = cursor.fetchall()
        return build_from_records(models.Trade, records)

    @classmethod
    def find_by_stock_marker(cls, marker: str, cursor: object):
        cursor.execute("""select * from stocks where stock_marker = %s;""", (marker,))
        stock = cursor.fetchone()
        return build_from_record(Stock, stock)
    
    @classmethod
    def find_by_company_name(cls, name: str, cursor: object):
        cursor.execute("""select * from stocks where company_name ILIKE %s;""", (f'%{name}%',))
        records = cursor.fetchall()
        return records