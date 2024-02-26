import backend.api.models as models
from backend.api.lib.orm import build_from_record

class Trade(models.BaseClass):
    __table__ = 'trades'
    attributes = ['id', 'stock_id', 'politician_id', 'purchased_or_sold', 'transaction_date', 'amount']

    def stock(self, cursor):
        cursor.execute("""select * from stocks where id = %s;""", (self.stock_id,))
        record = cursor.fetchone()
        return build_from_record(models.Stock, record)

    def politician(self, cursor):
        cursor.execute("""select * from politicians where id = %s;""", (self.politician_id,))
        record = cursor.fetchone()
        return build_from_record(models.Politician, record)

    def to_json(self, cursor):
        politician_name = self.politician(cursor).name 
        stock_marker = self.stock(cursor).stock_marker 
        return {'politician': politician_name, 
                'stock': stock_marker, 
                'purchased_or_sold': self.purchased_or_sold, 
                'transaction_date': self.transaction_date, 
                'amount': self.amount}



