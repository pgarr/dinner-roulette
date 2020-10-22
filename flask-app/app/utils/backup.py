import datetime
import json
import logging
import time

from flask import current_app
from sqlalchemy import MetaData

from app import db
from app.utils.email import send_email
from app.utils.thread_killer import GracefulKiller

logger = logging.getLogger('backup')
logger.setLevel(logging.INFO)


class BackupScheduler:

    def __init__(self, schedule_time):
        self.killer = GracefulKiller()
        self.wait_time = schedule_time
        logger.info("Schedule time - %d" % self.wait_time)

    def dump_backup(self):
        """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
        meta = MetaData()
        meta.reflect(bind=db.engine)
        dmp = {}
        for table in meta.sorted_tables:
            dmp[table.name] = [dict(row) for row in db.engine.execute(table.select())]
        return json.dumps(dmp, default=str)

    def dump_backup_flask(self):
        """Dump all tables as dict (table name : list (row) of dicts(column_name : value)"""
        tables = db.get_tables_for_bind()  # is unsorted (bad for testing)
        dmp = {}
        for table in tables:
            dmp[table.name] = [dict(row) for row in db.engine.execute(table.select())]
        return json.dumps(dmp)

    def send(self, dmp):
        title = "Dump " if not current_app.debug and not current_app.testing else "Test "
        title_today = title + datetime.date.today().strftime("%B %d, %Y")

        send_email(subject=title_today, sender=current_app.config['ADMINS'][0], recipients=current_app.config['ADMINS'],
                   text_body=None,
                   html_body=None,
                   attachments=[("Dump.json", "application/json", dmp)])

    def start(self):
        logger.info('Backup scheduler started')
        while not self.killer.kill_now:
            logger.info("Starting dump...")
            dmp = self.dump_backup()
            self.send(dmp)
            logger.info("Sent, going to sleep...")
            time.sleep(self.wait_time)
        logger.info('Backup scheduler stopped gracefully')
