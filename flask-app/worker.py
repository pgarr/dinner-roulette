from app import create_app
from app.utils.backup import BackupScheduler

if __name__ == "__main__":
    app = create_app()
    app.app_context().push()

    if app.config['BACKUP_SCHEDULE']:
        backup = BackupScheduler(int(app.config['BACKUP_SCHEDULE']))
        backup.start()
