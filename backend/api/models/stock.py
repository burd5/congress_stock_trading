import api.models as models
from api.lib.db import build_from_record

class Stock(models.BaseClass):
    __table__ = 'stocks'
    attributes = ['id', 'stock_marker', 'company_name']

    @classmethod
    def find_by_stock_marker(cls, marker, cursor):
        cursor.execute("""select * from stocks where stock_marker = %s;""", (marker,))
        stock = cursor.fetchone()
        return build_from_record(Stock, stock)
    
    @classmethod
    def find_by_company_name(cls, name, cursor):
        cursor.execute("""select * from stocks where company_name ILIKE %s;""", (f'%{name}%',))
        records = cursor.fetchall()
        return records