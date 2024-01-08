import api.models as models
from api.lib.db import build_from_record

class Politician(models.BaseClass):
    __table__ = 'politicians'
    attributes = ['id', 'name', 'part_of_congress', 'political_party', 'office']

    def stocks(self):
        pass

    def trades(self):
        pass

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

    