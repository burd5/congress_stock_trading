import api.models as models

class Trade(models.BaseClass):
    __table__ = 'trades'
    attributes = ['stock_id', 'politician_id', 'purchased_or_sold', 'transaction_date', 'amount']

