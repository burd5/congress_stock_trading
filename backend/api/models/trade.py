import backend.api.models as models
from backend.api.lib.orm import build_from_record
from backend.api import db
from sqlalchemy.orm import relationship
from backend.api.lib.db import create_supabase_connection

class Trade(db.Model):
    __tablename__ = 'dev.stg_house_trades'
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
    def house_trades(cls, schema):
        supabase = create_supabase_connection(schema)
        house_trades_result = supabase.table('stg_house_trades').select("*").execute()
        house_trades_data = house_trades_result.__dict__['data']

        return house_trades_data
    
    @classmethod
    def senate_trades(cls, schema):
        supabase = create_supabase_connection(schema)
        senate_trades_result = supabase.table('stg_senate_trades').select("*").execute()
        senate_trades_data = senate_trades_result.__dict__['data']

        return senate_trades_data



