import subprocess
import time

import requests


class Aut:
    def __init__(self):
        self.python = 'D:\\pgarr\\Documents\\projects\\dinner-roulette\\flask-app\\venv\\Scripts\\python.exe'
        self.runner = 'D:\\pgarr\\Documents\\projects\\dinner-roulette\\flask-app\\run_test_app.py'
        self.url = 'http://127.0.0.1:5000'
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
