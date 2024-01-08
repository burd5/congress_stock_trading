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