import psycopg2
from flask import g, current_app
from settings import DATABASE, SUPA_USER, TEST_DB, HOST, SUPA_PASSWORD, SUPA_CONN_URL, SUPA_KEY
from backend.api.lib.orm import build_from_record
from supabase import create_client
from supabase.lib.client_options import ClientOptions

conn_string = f"host={HOST} port=5432 dbname={DATABASE} user={SUPA_USER} password={SUPA_PASSWORD} sslmode=require"
conn = psycopg2.connect(conn_string)
cursor = conn.cursor()
# test_conn = psycopg2.connect(dbname=TEST_DB, user=USER)
# test_cursor = test_conn.cursor()

def add_record_to_house_trades(record: list):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    statement = """INSERT INTO house_trades (owner, politician_name, stock_information, purchased_or_sold, transaction_date, report_date, amount)
                            VALUES(%s, %s, %s, %s, %s, %s, %s);"""
    print(statement, record)
    cursor.execute(statement, record)
    conn.commit()
    conn.close()

def add_record_to_senate_trades(record: list):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    statement = """INSERT INTO senate_trades (politician_name, transaction_date, owner, stock_ticker, asset_name, asset_type, purchased_or_sold, amount, comment)
                            VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s);"""
    print(statement, record)
    cursor.execute(statement, record)
    conn.commit()
    conn.close()

def add_asset_record(record: list):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    statement = """INSERT INTO stocks (company_name, asset_type)
                            VALUES(%s, %s);"""
    if not check_asset_existence(record):
        print(statement, record)
        cursor.execute(statement, record)
        conn.commit()
        conn.close()

def add_report_record(record: list):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    statement = """INSERT INTO report_links (link)
                            VALUES(%s);"""
    cursor.execute(statement, (record,))
    conn.commit()
    conn.close()

def check_asset_existence(record: dict):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    check_statement = """SELECT EXISTS(
                            SELECT 1 FROM stocks
                            WHERE company_name = %s 
                            AND asset_type = %s
                        );"""
    cursor.execute(check_statement, record)
    exists = cursor.fetchone()[0]
    conn.close()
    return exists

def check_report_link_existence(link:str):
    conn = psycopg2.connect(conn_string)
    cursor = conn.cursor()
    
    check_statement = """SELECT EXISTS(
                            SELECT 1 FROM report_links
                            WHERE link = %s
                        );"""
    cursor.execute(check_statement, (link,))
    exists = cursor.fetchone()[0]
    conn.close()
    return exists

def drop_all_tables(conn, cursor):
    tables = ['stocks', 'politicians', 'trades']
    for table in tables:
        cursor.execute(f"""DELETE FROM {table};""")
        conn.commit()

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

def get_db():
    if "db" not in g:
        g.db = psycopg2.connect(user = current_app.config['DB_USER'],
                    password = current_app.config['DB_PASSWORD'],
                    dbname = current_app.config['DB_NAME'])
    return g.db

def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()

def to_dict(obj):
        dict_ = {}
        for key in obj.__mapper__.c.keys():
            dict_[key] = getattr(obj, key)
        return dict_

def create_supabase_connection(schema):
    supabase_url = SUPA_CONN_URL
    supabase_key = SUPA_KEY
    opts = ClientOptions().replace(schema=schema)
    supabase = create_client(supabase_url, supabase_key, options=opts)
    
    return supabase