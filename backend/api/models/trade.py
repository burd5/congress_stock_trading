import backend.api.models as models
from backend.api.lib.orm import build_from_record
from backend.api import db
from sqlalchemy.orm import relationship
from backend.api.lib.db import create_supabase_connection, conn_string
import psycopg2

class Trade(db.Model):
    __tablename__ = 'dev.int_trades'
    attributes = ['id', 'politician_name', 'stock ticker', 'stock_information', 'purchased_or_sold', 'transaction_date', 'amount']

    id = db.Column(db.Integer, primary_key=True)
    politician_name = db.Column(db.Integer)
    # stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    stock_ticker = db.Column(db.String(150))
    stock_information = db.Column(db.String(150), nullable=False)
    purchased_or_sold = db.Column(db.String(150), nullable=False)
    transaction_date = db.Column(db.DateTime(100), nullable=False)
    amount = db.Column(db.String(150), nullable=False)

    # politician = relationship('Politician', back_populates='trades', overlaps='stocks,politicians')
    # stock = relationship('Stock', back_populates='trades', overlaps='politicians,stocks')

    @classmethod
    def trades(cls):
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("select * from dev.int_trades where EXTRACT(YEAR from transaction_date) = 2024 order by transaction_date desc")
        records = cursor.fetchall()
        conn.close()

        return records
    



