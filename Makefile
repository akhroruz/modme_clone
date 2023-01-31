mig:
	python3 manage.py makemigrations
	python3 manage.py migrate

unmig:
	find . -path "*/migrations/*.py" -not -name "__init__.py" -delete

local:
	python3 manage.py makemessages -l en
	python3 manage.py makemessages -l ru
	python3 manage.py makemessages -l uz
	python3 manage.py compilemessages

admin:
	python3 manage.py createsuperuser --username admin --password admin@example.com

cs:
	python3 manage.py createsuperuser
