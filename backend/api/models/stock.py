import backend.api.models as models
from backend.api.lib.orm import build_from_record, build_from_records
import backend.api.models as models
from backend.api import db
from sqlalchemy.orm import relationship
import yfinance as yf
from datetime import datetime, timedelta
import pandas as pd

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
    def find_by_stock_marker(cls, marker: str, cursor: object):
        cursor.execute("""select * from stocks where stock_marker = %s;""", (marker,))
        stock = cursor.fetchone()
        return build_from_record(Stock, stock)
    
    @classmethod
    def find_by_company_name(cls, name: str, cursor: object):
        cursor.execute("""select * from stocks where company_name ILIKE %s;""", (f'%{name}%',))
        records = cursor.fetchall()
        return build_from_records(Stock, records)
    
    @classmethod
    def find_stock_history(cls, name:str, start_date:str, end_date:str=None):
        if '.' in name: name = name.replace('.', '-')
        start_date = datetime.strptime(start_date, '%Y-%m-%d')
        new_start_date = start_date - timedelta(days=180)
        new_start_date_str = new_start_date.strftime('%Y-%m-%d')
        new_end_date = datetime.now().date()
        new_end_date_str = new_end_date.strftime('%Y-%m-%d')
        data = yf.download(name, start=new_start_date_str, end=new_end_date_str)
        data.index = data.index.astype(str)
        
        return data.to_dict(orient='index')