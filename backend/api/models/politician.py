import api.models as models
from api.lib.db import build_from_record

class Politician(models.BaseClass):
    __table__ = 'politicians'
    attributes = ['id', 'name', 'part_of_congress', 'political_party', 'office']

    @classmethod
    def find_by_name_and_office(cls, name, office, cursor):
        cursor.execute("""select * from politicians where name = %s and office = %s;""", (name, office,))
        politician = cursor.fetchone()
        return build_from_record(Politician, politician)

    