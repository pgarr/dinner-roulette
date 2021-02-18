import os

flask_path = './../flask-app'

source_path = os.path.join(flask_path, 'requirements.txt')
destination_path = os.path.join(flask_path, 'requirements-jenkins.txt')

with open(source_path) as source_file:
    lines = source_file.readlines()

    with open(destination_path, 'w') as destination_file:
        for line in lines:
            if 'Heroku only' in line:
                break
            destination_file.write(line)
