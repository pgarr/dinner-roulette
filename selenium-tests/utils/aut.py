import os
import subprocess
import time

import requests


class Aut:
    def __init__(self):
        self.python = os.environ.get('PYTHON_AUT_DIR')
        self.runner = os.environ.get('AUT_DIR')
        self.url = 'http://127.0.0.1:' + os.environ.get('AUT_PORT')
        self.process = None

    def run(self, timeout=30):
        self.process = subprocess.Popen([self.python, self.runner])
        for i in range(timeout):
            time.sleep(1)
            try:
                response = requests.get(self.url)
            except Exception:
                continue
            if response.ok:
                return
        raise TimeoutError('Application not ready after timeout')

    def stop(self):
        if self.process:
            self.process.terminate()
