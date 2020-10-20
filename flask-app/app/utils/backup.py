import datetime
import json
import time
from threading import Thread

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from app.utils.email import send_email


class BackupScheduler:

    def __init__(self, db: SQLAlchemy, schedule_time):
        self.app = current_app._get_current_object()
        self.db = db
        self.wait_time = schedule_time
        self.app.logger.info("Backup: schedule time - %d" % self.wait_time)

    def dump_backup(self):
        """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
        meta = MetaData()
        meta.reflect(bind=self.db.engine)
        dmp = {}
        for table in meta.sorted_tables:
            dmp[table.name] = [dict(row) for row in self.db.engine.execute(table.select())]
        return json.dumps(dmp, default=str)

    def dump_backup_flask(self):
        """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
        tables = self.db.get_tables_for_bind()  # is unsorted (bad for testing)
        dmp = {}
        for table in tables:
            dmp[table.name] = [dict(row) for row in self.db.engine.execute(table.select())]
        return json.dumps(dmp)

    def send(self, dmp):
        title = "Dump " if not self.app.debug and not self.app.testing else "Test "
        title_today = title + datetime.date.today().strftime("%B %d, %Y")

        send_email(subject=title_today, sender=self.app.config['ADMINS'][0], recipients=self.app.config['ADMINS'],
                   text_body=None,
                   html_body=None,
                   attachments=[("Dump.json", "application/json", dmp)])

    def send_async_dumps_periodically(self):
        with self.app.app_context():
            while True:
                self.app.logger.info("Backup: starting dump...")
                dmp = self.dump_backup()
                self.send(dmp)
                self.app.logger.info("Backup: sent, going to sleep...")
                time.sleep(self.wait_time)

    def start(self):
        Thread(target=self.send_async_dumps_periodically, daemon=True).start()
