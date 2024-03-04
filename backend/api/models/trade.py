import backend.api.models as models
from backend.api.lib.orm import build_from_record
from backend.api import db
from sqlalchemy.orm import relationship

class Trade(db.Model):
    __tablename__ = 'trades'
    attributes = ['id', 'stock_id', 'politician_id', 'purchased_or_sold', 'transaction_date', 'amount']

    id = db.Column(db.Integer, primary_key=True)
    stock_id = db.Column(db.Integer, db.ForeignKey('stocks.id'))
    politician_id = db.Column(db.Integer, db.ForeignKey('politicians.id'))
    purchased_or_sold = db.Column(db.String(150), nullable=False)
    transaction_date = db.Column(db.DateTime(100), nullable=False)
    amount = db.Column(db.String(150), nullable=False)

    politician = relationship('Politician', back_populates='trades', overlaps='stocks,politicians')
    stock = relationship('Stock', back_populates='trades', overlaps='politicians,stocks')



