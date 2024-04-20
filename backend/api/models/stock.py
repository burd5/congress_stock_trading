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

        while transaction_date.weekday() >= 5:
        # If the date is Saturday (5) or Sunday (6), increment by one day
            transaction_date += timedelta(days=1)

        transaction_date_str = transaction_date.strftime('%Y-%m-%d')
        
        new_start_date = transaction_date - timedelta(days=180)
        new_start_date_str = new_start_date.strftime('%Y-%m-%d')

        new_end_date = datetime.now().date()
        while new_end_date.weekday() >= 5:
        # If the date is Saturday (5) or Sunday (6), increment by one day
            new_end_date -= timedelta(days=1)

        new_end_date_str = new_end_date.strftime('%Y-%m-%d')
        data = yf.download(name, start=new_start_date_str)
        
        current_price = data.loc[new_end_date_str, 'Close']
        transaction_price = data.loc[transaction_date_str, 'Close']

        percent_difference = round(((current_price - transaction_price) / transaction_price) * 100, 2)

        data.index = data.index.astype(str)
        
        return data.to_dict(orient='index'), percent_difference