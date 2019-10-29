import datetime
import json
import time
from threading import Thread

from flask import current_app
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData

from app.email import send_email

4


class BackupScheduler:

    def __init__(self, db: SQLAlchemy):
        self.app = current_app._get_current_object()
        self.db = db
        self.wait_time = int(self.app.config['BACKUP_SCHEDULE'])
        self.app.logger.info("Backup: schedule time - %d" % self.wait_time)

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

    def send(self, dmp):
        title_today = "Dump " + datetime.date.today().strftime("%B %d, %Y")
        send_email(title_today, sender=self.app.config['ADMINS'][0], recipients=self.app.config['ADMINS'],
                   text_body=None,
                   html_body=None,
                   attachment_tuple=("Dump.json", "application/json", dmp))  # TODO: create some body

    def send_async_dumps_periodically(self):
        with self.app.app_context():
            while True:
                self.app.logger.info("Backup: starting dump...")
                dmp = self.dump_backup()
                self.send(dmp)
                self.app.logger.info("Backup: done, going to sleep...")
                time.sleep(self.wait_time)

    def start(self):
        Thread(target=self.send_async_dumps_periodically).start()
        # TODO: ctrl + c does not work with this thread up
