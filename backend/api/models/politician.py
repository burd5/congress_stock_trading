import api.models as models
from api.lib.db import build_from_record, build_from_records, cursor

class Politician(models.BaseClass):
    __table__ = 'politicians'
    attributes = ['id', 'name', 'part_of_congress', 'state', 'political_party', 'office_marker']

    def stocks(self):
        cursor.execute(f"""select s.* from stocks s join trades t
                            on s.id = t.stock_id
                            where t.politician_id = %s;""", (self.id,))
        records = cursor.fetchall()
        return build_from_records(models.Stock, records)

    def trades(self):
        cursor.execute(f"""select *
                            from trades
                            where politician_id = %s;""", (self.id,))
        records = cursor.fetchall()
        return build_from_records(models.Trade, records)

    @classmethod
    def find_by_name_house(cls, name: str, cursor: object):
        cursor.execute("""select * from politicians where name = %s;""", (name, ))
        politician = cursor.fetchone()
        return build_from_record(Politician, politician)
    
    @classmethod
    def find_by_name_senate(cls, name: str, cursor: object):
        cursor.execute("""select * from politicians where name = %s and part_of_congress = 'Senate';""", (name, ))
        politician = cursor.fetchone()
        return build_from_record(Politician, politician)
    
    @classmethod
    def find_by_office(cls, office: str, name: str, cursor: object):
        cursor.execute("""select * from politicians where name = %s and office = %s;""", (name, office,))
        politician = cursor.fetchone()
        return build_from_record(Politician, politician)

    