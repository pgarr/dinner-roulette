import datetime
import json

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from app.email import send_email


class BackupHandler:

    def __init__(self, db: SQLAlchemy, sender, recipients):
        self.db = db
        self.sender = sender
        self.recipients = recipients

    def dump_backup(self):
        """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
        meta = MetaData()
        meta.reflect(bind=self.db.engine)
        dmp = {}
        for table in meta.sorted_tables:
            dmp[table.name] = [dict(row) for row in self.db.engine.execute(table.select())]
        return json.dumps(dmp)

    def dump_backup_flask(self):
        """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
        tables = self.db.get_tables_for_bind()  # TODO: is unsorted (bad for testing)
        dmp = {}
        for table in tables:
            dmp[table.name] = [dict(row) for row in self.db.engine.execute(table.select())]
        return json.dumps(dmp)

    def send_dump(self):
        dmp = self.dump_backup()
        title_today = "Dump " + datetime.date.today().strftime("%B %d, %Y")
        send_email(title_today, sender=self.sender, recipients=self.recipients,
                   text_body=None,
                   html_body=None, attachment_tuple=("Dump.json", "application/json", dmp))  # TODO: create some body
