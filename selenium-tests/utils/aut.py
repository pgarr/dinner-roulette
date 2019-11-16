import json
import os
import subprocess
import time

import requests


class Aut:
    def __init__(self, users=None, recipes=None, waiting_recipes=None):
        self.python = os.environ.get('PYTHON_AUT_DIR')
        self.runner = os.environ.get('AUT_DIR')
        self.url = 'http://127.0.0.1:' + os.environ.get('AUT_PORT')
        self.process = None
        self.setUp_input_data = self.prepare_input_data(users=users, recipes=recipes, waiting_recipes=waiting_recipes)

    def run(self, timeout=30):
        args = [self.python, self.runner]
        if self.setUp_input_data:
            args.append('-i')
            args.append(self.setUp_input_data)
        self.process = subprocess.Popen(args)
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

    def prepare_input_data(self, users, recipes, waiting_recipes):  # TODO: requires unit tests
        if not users and not recipes and not waiting_recipes:
            return None
        else:
            dict_data = {}
            if users:
                dict_data['users'] = users
            if recipes:
                dict_data['recipes'] = recipes
            if waiting_recipes:
                dict_data['waiting_recipes'] = waiting_recipes
            input_data = json.dumps(dict_data)
            input_data.replace('"', '/"')
            return input_data
