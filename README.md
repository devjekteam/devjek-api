# Flask API #2 (Cool name TBD)

Functions very similarly to Consultation Kit. Uses Python 3.5 and Postgresql

### Structure

- ***run.py*** entry point to start the API
- ***manage.py*** Alembic auto migration code (see Migrations Section)
- ***webapp/*** contains source code for app
- ***webapp/routes*** contains api routes and [View Functions](http://flask.pocoo.org/docs/0.12/blueprints/)
- ***webapp/routes/__init__.py*** contains base blueprint and initializes routes
- ***webapp/model.py*** contains SQLAlchemy models that talk to db (postgresql). Alembic can run automatic migrations based on changes in this file. (see Migrations section)
- ***webapp/app.py*** contains app factory function that creates instance of this API
- ***webapp/db.py*** contains shared db instance. Watch out for app context when connecting to db.

### Quick start

- Set up virtual environment (highly recommended)

```
pip install virtualenv
virtualenv --python=<PATH TO PYTHON BINARY>(e.g. /usr/local/bin/python3.5) .venv
source .venv/bin/activate
```

- Install dependencies

```
pip install -r requirements.txt
```

- Create a postgresql db for your API. Either create an environment variable `SQLALCHEMY_DATABASE_URI` that has the name of your DB or just make it named `devjekdev` and the app will find it.

- Initialize Alembic

```
python manage.py db init
```

- Run migrations

```
python manage.py db upgrade
```

- Start app
```
python run.py
```

### Migrations

We use Alembic + SQLAlchemy which is able to autodetect changes in `webapp/model.py` and create new migrations based off of code changes. If you make changes to model.py and want to create a new migration run:

```
python manage.py db migrate
```

Make sure you check your new migration for accuracy and add a description on the top line.

Next run an upgrade

```
python manage.py db upgrade
```

If you need to run a downgrade use

```
python manage.py db downgrade
```

DO NOT EDIT EXISTING MIGRATIONS UNLESS YOU ARE SURE OF WHAT YOU ARE DOING.

If things get super jacked up and alembic doesn't let you downgrade you can always delete your db but this isn't ideal for obvious reasons.

### Tests

Entire Test Suite
```
./tests.sh
```

Single Test
```
./tests unit_tests/<test_file>.py
```

### Production

You will need to set some env variables for Production

```
APP_ENV=production
```
