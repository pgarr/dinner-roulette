# dinner-roulette

## What's this?

Web app to store dishes recipes.
It has users who create recipes and admin who accepts them before they are visible for others.

Project contains separated frontend and backend RESTful API. 
Frontend is created in React.js.
Backend is created in Python, uses Flask and SQLAlchemy.

## Useful commands.

### Push only flask-app folder to Heroku.

  --git subtree push --prefix flask-app heroku master

### Updates for translations (Flask-Babel).

In flask-app folder:

  --(venv) $ pybabel extract -F babel.cfg -k _l -o messages.pot .

  --(venv) $ pybabel update -i messages.pot -d app/translations

This creates new messages.pot file and merges it into all messages.po files for all languages in the project.
After this, you can translate new entries in messages.po files and use:

  --flask translate compile

This operation adds a messages.mo file next to messages.po in each language repository. The .mo file is the file that Flask-Babel will use to load translations for the application.

### Updates for database structure (Flask-Migrate).

  --flask db migrate

This operation generates a new migration script.

  --flask db upgrade

This operation applies the changes to database.

  --flask db downgrade

This command undoes the last migration (mostly used in development phase).
