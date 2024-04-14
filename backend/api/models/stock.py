import backend.api.models as models
from backend.api.lib.orm import build_from_record, build_from_records
import backend.api.models as models
from backend.api import db
from backend.api.lib.db import conn_string
from sqlalchemy.orm import relationship
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd
import psycopg2

class Stock(db.Model):
    __tablename__ = 'stocks'
    attributes = ['id', 'stock_marker', 'company_name', 'asset_type']

    id = db.Column(db.Integer, primary_key=True)
    stock_marker = db.Column(db.String(150), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    asset_type = db.Column(db.String(150), nullable=False)

    # trades = relationship('Trade', back_populates='stock', cascade='all, delete-orphan')
    # politicians = db.relationship('Politician', secondary='trades', overlaps='trades,stocks')

    @classmethod
    def find_by_stock_marker(cls, marker: str):
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute("""select * from dev.stg_stocks where stock_marker = %s;""", (marker,))
        stock = cursor.fetchone()
        return stock
    
    @classmethod
    def find_by_company_name(cls, name: str, cursor: object):
        cursor.execute("""select * from stocks where company_name ILIKE %s;""", (f'%{name}%',))
        records = cursor.fetchall()
        return build_from_records(Stock, records)
    
    @classmethod
    def find_stock_history(cls, name:str, start_date:str, end_date:str=None):
        decoded_date = '-'.join(start_date.split('%2F'))
        month, day, year = decoded_date.split('-')
        if '.' in name: name = name.replace('.', '-')
        transaction_date = datetime.strptime(f'{year}-{month}-{day}', '%Y-%m-%d')
        new_start_date = transaction_date - timedelta(days=180)
        new_start_date_str = new_start_date.strftime('%Y-%m-%d')
        new_end_date = datetime.now().date()
        new_end_date_str = new_end_date.strftime('%Y-%m-%d')
        data = yf.download(name, start=new_start_date_str, end=new_end_date_str)
        data.index = data.index.astype(str)

             # Calculate the close price of the transaction date
        if transaction_date.strftime('%Y-%m-%d') in data.index:
            transaction_close_price = data.loc[transaction_date.strftime('%Y-%m-%d')]['Close']
        else:
            transaction_close_price = None
        
        # Calculate the current close price (last price)
        if len(data) > 0:
            current_close_price = data['Close'].iloc[-1]
        else:
            current_close_price = None
        
        # Calculate performance percentage if prices are available
        if transaction_close_price is not None and current_close_price is not None:
            performance_percentage = ((current_close_price - transaction_close_price) / transaction_close_price) * 100
        else:
            performance_percentage = None
        
        
        return data.to_dict(orient='index'), performance_percentage