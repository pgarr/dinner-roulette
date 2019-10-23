import json

from sqlalchemy import MetaData

from app import db


def dump_backup():
    """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
    meta = MetaData()
    meta.reflect(bind=db.engine)
    dmp = {}
    for table in meta.sorted_tables:
        dmp[table.name] = [dict(row) for row in db.engine.execute(table.select())]
    return json.dumps(dmp)


def dump_backup_flask():
    """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
    tables = db.get_tables_for_bind()
    dmp = {}
    for table in tables:  # TODO: is unsorted (bad for testing)
        dmp[table.name] = [dict(row) for row in db.engine.execute(table.select())]
    return json.dumps(dmp)
