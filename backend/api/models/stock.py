import backend.api.models as models
from backend.api.lib.orm import build_from_record, build_from_records
import backend.api.models as models
from backend.api import db
from sqlalchemy.orm import relationship

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