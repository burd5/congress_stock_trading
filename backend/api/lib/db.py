import psycopg2
from settings import DATABASE, USER, TEST_DB
conn = psycopg2.connect(dbname=DATABASE, user=USER)
cursor = conn.cursor()
test_conn = psycopg2.connect(dbname=TEST_DB, user=USER)
test_cursor = test_conn.cursor()

def build_from_record(Class, record):
    if not record: return None
    attrs = dict(zip(Class.attributes, record))
    obj = Class()
    obj.__dict__ = attrs
    return obj

def build_from_records(Class, records):
    return [build_from_record(Class, record) for record in records]

def add_record_to_database(record: list, user: str, database: str):
    conn = psycopg2.connect(user=user, database=database)
    cursor = conn.cursor()
    statement = """INSERT INTO trades (stock_id, politician_id, purchased_or_sold, transaction_date, amount)
                            VALUES(%s, %s, %s, %s, %s);"""
    if not check_record_existence(record, user, database):
        print(statement, record)
        cursor.execute(statement, record)
        conn.commit()
        conn.close()

def check_record_existence(record: dict, user: str, database: str):
    conn = psycopg2.connect(user=user, database=database)
    cursor = conn.cursor()
    
    check_statement = """SELECT EXISTS(
                            SELECT 1 FROM trades
                            WHERE stock_id = %s 
                            AND politician_id = %s
                            AND purchased_or_sold = %s
                            AND transaction_date = %s 
                            AND amount = %s
                        );"""
    cursor.execute(check_statement, record)
    exists = cursor.fetchone()[0]
    conn.close()
    return exists

def find_all(Class):
    cursor.execute(f"""select * from {Class.__table__};""")
    records = cursor.fetchall()
    return build_from_records(Class, records)

def find(Class, id):
    cursor.execute(f"""select * from {Class.__table__} where id = %s;""", (id,))
    record = cursor.fetchone()
    return build_from_record(Class, record)

def drop_all_tables(test_conn, test_cursor):
    tables = ['trades', 'stocks', 'politicians']
    for table in tables:
        test_cursor.execute(f"""TRUNCATE {table} RESTART IDENTITY;""")
        test_conn.commit()

def save(obj, conn, cursor):
    s_str = ', '.join(len(values(obj)) * ['%s'])
    venue_str = f"""INSERT INTO {obj.__table__} ({keys(obj)}) VALUES ({s_str});"""
    cursor.execute(venue_str, list(values(obj)))
    conn.commit()
    cursor.execute(f'SELECT * FROM {obj.__table__} ORDER BY id DESC LIMIT 1')
    record = cursor.fetchone()
    return build_from_record(type(obj), record)

def keys(obj):
    venue_attrs = obj.__dict__
    selected = [attr for attr in obj.attributes if attr in venue_attrs.keys()]
    return ', '.join(selected)

def values(obj):
    venue_attrs = obj.__dict__
    return [venue_attrs[attr] for attr in obj.attributes if attr in venue_attrs.keys()]