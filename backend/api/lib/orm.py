def build_from_record(Class, record):
    if not record: return None
    attrs = dict(zip(Class.attributes, record))
    obj = Class()
    obj.__dict__ = attrs
    return obj

def build_from_records(Class, records):
    return [build_from_record(Class, record) for record in records]

def find_all(cursor, Class):
    cursor.execute(f"""select * from {Class.__table__};""")
    records = cursor.fetchall()
    return build_from_records(Class, records)

def find(cursor, Class, id):
    cursor.execute(f"""select * from {Class.__table__} where id = %s;""", (id,))
    record = cursor.fetchone()
    return build_from_record(Class, record)