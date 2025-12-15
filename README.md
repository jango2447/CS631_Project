Download posrt gresql from here https://www.postgresql.org/download/
postgres password "cs631"
port 5432

open pgadmin
right click databases -> create -> Database...
name the database "cs631_personnel_db" click save
create a new user/role
go to login/group roles -> create -> login/group role...
username "cs631_user"
in definition set password to "cs631"
in privileges select "superuser" and "can login"

open terminal send
pip install Flask-Migrate
pip install psycopg2-binary

run terminal from Repos\CS631_Project\CS631_Project\CS631_Project> flask db migrate
$env:FLASK_APP = "manage.py"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade
now the database is populated with tables

how to change the database tables
flask db migrate -m "Describe your change"
flask db upgrade -Apply the migration
flask db downgrade -Roll back the most recent migration

how to add data
\Repos\CS631_Project\CS631_Project\CS631_Project> flask seed-db
flask seed-db

How to start the web application
send $env:FLASK_APP="manage.py"
Repos\CS631_Project\CS631_Project> $env:FLASK_APP="manage.py"
send flask run
Repos\CS631_Project\CS631_Project> flask run
