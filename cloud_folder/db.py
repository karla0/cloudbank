import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext



# gets database configured in init file
def get_db():
    """Creates connection to configued database and adds it to g variable

    Returns:
        Connection: SQLite connection to database to use for executing SQL queries
    """
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# closes connection to database
def close_db(e=None):
    """ Removes database from g variable and closes connection."""
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    """Initializes the database"""

    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
@with_appcontext
def init_db_command():
    """Clears the exisiting data, and creates new database according to schema
    """
    init_db()
    click.echo('Initalized the database.')

def init_app(app):
    # funtion to run during clean up after return response
    app.teardown_appcontext(close_db)
    # adding a new command to be called with flask
    app.cli.add_command(init_db_command)

