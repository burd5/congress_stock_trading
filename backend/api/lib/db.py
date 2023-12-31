import psycopg2
from settings import DATABASE, USER

conn = psycopg2.connect(dbname=DATABASE, user=USER)
cursor = conn.cursor()

def build_from_record(Class, record):
    if not record: return None
    attrs = dict(zip(Class.attributes, record))
    obj = Class()
    obj.__dict__ = attrs
    return obj
