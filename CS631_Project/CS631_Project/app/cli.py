
import click
from flask.cli import with_appcontext
from .models import db, Employee

@click.command(name='seed-db')
@with_appcontext
def seed_db():
    # Add demo data here
    e1 = Employee(employee_no=1, employee_name='John Doe')
    db.session.add(e1)
    db.session.commit()
    click.echo('Seeded the database!')

def register_commands(app):
    app.cli.add_command(seed_db)
