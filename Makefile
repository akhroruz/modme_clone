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

load:
	python3 manage.py loaddata role

faker:
	python3 manage.py create -c 2 -b 5 -course 5 -r 10 -hd 10 -u 10 -a 10 -li 10 -l 10 -gr 10

setup:
	pip install -r requirements.txt

poetry:
	curl -sSL https://install.python-poetry.org | python3 -

admin:
	python3 manage.py createsuperuser --noinput

remig:
	make unmig
	make mig
	make admin
	make faker
