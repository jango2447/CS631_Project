password cs631

pip install Flask-Migrate
cd .\CS631_Project\
$env:FLASK_APP = "manage.py"
flask db init
flask db migrate -m "Initial migration"
flask db upgrade