import backend.api.models as models
from backend.api.lib.orm import build_from_record, build_from_records
from backend.api import db
from sqlalchemy.orm import relationship
from backend.api.lib.db import create_supabase_connection, conn_string
import psycopg2

class Politician(db.Model):
    __tablename__ = 'public.politicians'
    attributes = ['id', 'name', 'part_of_congress', 'state', 'political_party', 'office']

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), unique=True, nullable=False)
    part_of_congress = db.Column(db.String(80), nullable=False)
    state = db.Column(db.String(150), nullable=False)
    political_party = db.Column(db.String(80), nullable=False)
    office = db.Column(db.String(30), nullable=False)

    # trades = relationship('Trade', back_populates='politician', cascade='all, delete-orphan')
    # stocks = db.relationship('Stock', secondary='trades', overlaps='trades')

    @classmethod
    def find_by_name_house(cls, name: str, cursor: object):
        cursor.execute("""select * from politicians where name = %s and part_of_congress = 'House';""", (name, ))
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

    @classmethod
    def politician(cls, id):
        conn = psycopg2.connect(conn_string)
        cursor = conn.cursor()
        cursor.execute(f"select * from dev.stg_politicians where id = {int(id)}")
        record = cursor.fetchone()
        conn.close()

        return record